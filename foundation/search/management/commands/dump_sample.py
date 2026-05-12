"""Dump a representative slice of CMS data as a Django fixture.

Why this exists:
    A full `manage.py dumpdata` of the production-flavored DB produces a
    ~57 MB JSON file — too big to be useful as a test fixture. This command
    picks a coherent subtree (the home page + its first N descendants)
    and walks the FK graph so the resulting fixture is self-consistent
    and small enough to load in tests.

What it does:
    1. Picks the first --max-pages cms.Page rows by id (default 100). Page
       1 and 2 are the home pages, so the slice always includes the home.
    2. Collects PKs for every model that has a direct FK into the selected
       pages: TreeNode, Title, Placeholder, CMSPlugin (and its concrete
       per-plugin tables).
    3. Adds the small reference-data models (Site, PageType, etc.) in
       full — they're tiny and tests need them.
    4. Serializes everything as a single Django JSON fixture using
       `--natural-foreign --natural-primary` so the fixture survives
       PK changes between runs.

Usage:
    python manage.py dump_sample
    python manage.py dump_sample --max-pages 50 --out fixtures/small.json
"""
from __future__ import annotations

import io
import os
import re
import unicodedata
from collections import OrderedDict

from django.core.management.base import BaseCommand
from django.core import serializers
from django.apps import apps


DEFAULT_OUT = "foundation/tests/fixtures/sample_data.json"


# Use fake names to anonymize the names
# that appear in `card_person.CardPerson` rows so the committed fixture
# doesn't carry real OKFN team identities.
FAKE_NAMES = [
    "Cachi Zelaya",
    "Daniel Willington",
    "Luis Galván",
    "Daniel Valencia",
    "Pablo Guiñazú",
    "Fabián Reynoso",
    "Gonzalo Klusener",
    "Julian Maidana",
    "Guido Herrera",
    "Javier Gandolfi",
    "Mario Cuenca"
]


def _email_slug(name: str) -> str:
    """Lowercase ASCII slug suitable for the local part of an email."""
    n = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return ".".join(n.lower().split())


class Command(BaseCommand):
    help = "Dump a representative slice of CMS data as a Django fixture."

    def add_arguments(self, parser):
        parser.add_argument(
            "--max-pages",
            type=int,
            default=100,
            help=(
                "How many cms.TreeNode rows to include (default: 100). "
                "Each treenode typically owns a draft + published Page, "
                "so 100 treenodes produces ~200 pages — roughly 30%% of "
                "a 622-page production DB."
            ),
        )
        parser.add_argument(
            "--out",
            default=DEFAULT_OUT,
            help=f"Output path (default: {DEFAULT_OUT}).",
        )

    def handle(self, *args, **opts):
        from cms.models import Page, Title, Placeholder, CMSPlugin, TreeNode

        max_pages = opts["max_pages"]
        out_path = opts["out"]

        # Select TreeNodes ordered by `path` (treebeard MP_Node). Lexicographic
        # path order is topological: any node's ancestors have a strictly
        # shorter path that's a prefix, so they come earlier in the ordering.
        # Slicing to N still yields a self-consistent forest — no orphaned
        # parent_id references when we load it back as a fixture.
        treenode_pks = list(
            TreeNode.objects.order_by("path").values_list("pk", flat=True)[:max_pages]
        )
        page_pks = list(
            Page.objects.filter(node__in=treenode_pks)
            .values_list("pk", flat=True)
        )
        # Page has a self-FK `publisher_public` (draft <-> published pair).
        # Some pages in the slice may reference a partner outside it; we
        # rely on Django's loaddata to leave that FK as the value in JSON
        # if the partner is also in the fixture, otherwise the slice still
        # loads (the FK is nullable and unused for fixture-driven tests).

        self.stdout.write(f"Selected {len(treenode_pks)} treenodes -> {len(page_pks)} pages")

        title_pks = list(Title.objects.filter(page__in=page_pks).values_list("pk", flat=True))
        placeholder_pks = list(
            Placeholder.objects.filter(page__in=page_pks).values_list("pk", flat=True)
        )

        # Plugins live on placeholders. CMSPlugin is the abstract parent;
        # each concrete plugin type has its own table that inherits from it.
        # We pick all CMSPlugin rows in the selected placeholders, then for
        # every concrete plugin model we find the rows whose `cmsplugin_ptr_id`
        # is in our plugin set. This is what makes the fixture self-consistent.
        plugin_pks = list(
            CMSPlugin.objects.filter(placeholder__in=placeholder_pks)
            .values_list("pk", flat=True)
        )
        self.stdout.write(
            f"Walked relations: {len(treenode_pks)} treenodes, "
            f"{len(title_pks)} titles, {len(placeholder_pks)} placeholders, "
            f"{len(plugin_pks)} plugins"
        )

        # Concrete plugin models — anything that subclasses CMSPlugin.
        concrete_plugin_models = [
            m for m in apps.get_models()
            if issubclass(m, CMSPlugin) and m is not CMSPlugin
        ]

        # Walk filer FKs from the concrete plugins. Many CMS plugins (Picture,
        # OKImage, Video, Gallery, Banner, ...) hold ForeignKeys into
        # filer.File / filer.Image, and a fixture that omits them fails
        # constraint checks at load time. We collect every referenced
        # filer.File / filer.Image, then walk filer.Folder up to the roots so
        # the folder tree is also self-consistent.
        from filer.models import File as FilerFile, Image as FilerImage, Folder
        from django.db.models import ForeignKey

        filer_file_pks = set()
        filer_image_pks = set()
        for m in concrete_plugin_models:
            qs = m.objects.filter(cmsplugin_ptr_id__in=plugin_pks)
            for f in m._meta.get_fields():
                if not isinstance(f, ForeignKey):
                    continue
                rel_label = f.related_model._meta.label
                if rel_label not in ("filer.File", "filer.Image"):
                    continue
                ids = {pk for pk in qs.values_list(f.attname, flat=True) if pk}
                if rel_label == "filer.Image":
                    filer_image_pks |= ids
                else:
                    filer_file_pks |= ids

        # filer.Image is multi-table-inherited from filer.File, so each
        # referenced Image needs its parent File row too.
        filer_file_pks |= set(
            FilerImage.objects.filter(pk__in=filer_image_pks)
            .values_list("file_ptr_id", flat=True)
        )

        # Walk Folder ancestors so every folder.parent_id resolves.
        folder_pks = set()
        to_check = set(
            FilerFile.objects.filter(pk__in=filer_file_pks)
            .exclude(folder__isnull=True)
            .values_list("folder_id", flat=True)
        )
        while to_check:
            folder_pks |= to_check
            parents = set(
                Folder.objects.filter(pk__in=to_check)
                .exclude(parent__isnull=True)
                .values_list("parent_id", flat=True)
            )
            to_check = parents - folder_pks

        self.stdout.write(
            f"Walked filer: {len(folder_pks)} folders, "
            f"{len(filer_file_pks)} files, {len(filer_image_pks)} images"
        )

        # Build the (model, queryset) list in load order. Loaddata will respect
        # natural keys; the order here is mostly cosmetic but mirrors load
        # dependencies (sites and types before pages, pages before titles, etc).
        plan = OrderedDict()

        # Reference data — small, dump in full. (cms.PageType deliberately
        # omitted: it's a proxy on cms.Page, so dumping it would duplicate
        # the rows we already emit for Page.)
        plan[apps.get_model("sites", "Site")] = apps.get_model("sites", "Site").objects.all()

        # Filer must come before plugins that reference it. filer.File uses
        # django-polymorphic, so a plain `.filter(...)` returns subclass
        # instances (Image) and they'd serialize as `filer.image`. Force
        # the base-table view with `.non_polymorphic()` so File rows really
        # come out as `filer.file` in the fixture.
        plan[Folder] = Folder.objects.filter(pk__in=folder_pks)
        plan[FilerFile] = FilerFile.objects.non_polymorphic().filter(pk__in=filer_file_pks)
        plan[FilerImage] = FilerImage.objects.filter(pk__in=filer_image_pks)

        # Selected slice.
        plan[TreeNode] = TreeNode.objects.filter(pk__in=treenode_pks)
        plan[Page] = Page.objects.filter(pk__in=page_pks)
        plan[Title] = Title.objects.filter(pk__in=title_pks)
        plan[Placeholder] = Placeholder.objects.filter(pk__in=placeholder_pks)
        plan[CMSPlugin] = CMSPlugin.objects.filter(pk__in=plugin_pks)
        for m in concrete_plugin_models:
            plan[m] = m.objects.filter(cmsplugin_ptr_id__in=plugin_pks)

        # Serialize one model at a time so we can report progress.
        # We also NULL out FKs to auth.User on the way out: filer.File and
        # filer.Folder both have an `owner` FK, but we don't want to ship
        # auth.User rows (PII: emails, hashed passwords). The owner field is
        # nullable and unused for fixture-driven tests.
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        all_objects = []
        for model, qs in plan.items():
            count = qs.count()
            if count == 0:
                continue
            self.stdout.write(f"  {model._meta.label:<40} {count:>6}")
            objs = list(qs)
            if model in (FilerFile, FilerImage, Folder):
                for o in objs:
                    o.owner_id = None
            all_objects.extend(objs)

        # Anonymize PII before serialization. card_person.CardPerson holds
        # real team names and emails; we map each unique name onto a famous
        # historic Talleres de Córdoba player and clear the bio + socials.
        # We also collect the original-name → player mapping for a
        # post-serialization sweep over text-bearing fields (e.g. HTML body
        # of djangocms_text_ckeditor.text rows that mention team members).
        person_label = "card_person.CardPerson"
        original_names = sorted({
            o.name for o in all_objects
            if o._meta.label == person_label and getattr(o, "name", None)
        })
        name_map = {
            n: FAKE_NAMES[i % len(FAKE_NAMES)]
            for i, n in enumerate(original_names)
        }
        for o in all_objects:
            if o._meta.label != person_label:
                continue
            new_name = name_map.get(o.name, o.name)
            o.name = new_name
            o.description = f"{new_name} is a member of the team."
            o.email = f"{_email_slug(new_name)}@example.com"
            o.url = ""
            o.x_account = ""

        # Some text plugins in the source DB contain board-meeting minutes
        # with attendee names and initials — those are internal documents
        # that should never have been in the published CMS. Detect by
        # signature phrases and replace the entire body with a placeholder.
        minutes_markers = (
            "Observers:",
            "Observing:",
            "Apologies:",
            "Apologies",
            "Trustees:",
            "Board meeting",
            "Minutes",
            "Present:",
            "Present</strong>",
            "(board observer)",
        )
        # Also catch bodies that have multiple `FirstName LastName (XX)`
        # initials-in-parens patterns — that shape is almost only used in
        # meeting minutes.
        initials_pattern = re.compile(r"\b[A-Z][a-zé]+\s+[A-Z][a-zé]+\s*\([A-Z]{1,4}\)")

        nuked_bodies = 0
        for o in all_objects:
            if o._meta.label != "djangocms_text_ckeditor.Text":
                continue
            body = getattr(o, "body", "") or ""
            if any(m in body for m in minutes_markers) or len(initials_pattern.findall(body)) >= 2:
                o.body = "<p>(text content removed during anonymization)</p>"
                nuked_bodies += 1
        if nuked_bodies:
            self.stdout.write(f"Nuked {nuked_bodies} minutes-style text bodies")

        # Serialize to a string buffer so we can scrub remaining PII in any
        # free-text field (rich-text plugin bodies, headings, list items).
        buf = io.StringIO()
        serializers.serialize(
            "json",
            all_objects,
            stream=buf,
            use_natural_foreign_keys=True,
            use_natural_primary_keys=True,
            indent=2,
        )
        text = buf.getvalue()

        # Replace each original name globally. Sort longest-first so e.g.
        # "Sara Petti" is replaced before any shorter substring match.
        for orig in sorted(name_map, key=len, reverse=True):
            text = text.replace(orig, name_map[orig])

        # Neutralize any okfn.org email that survived (e.g. info@okfn.org or
        # names embedded in HTML bodies that aren't on the card_person list).
        text = re.sub(r"[a-zA-Z0-9._%+-]+@okfn\.org", "noreply@example.com", text)

        with open(out_path, "w") as fh:
            fh.write(text)

        size_mb = os.path.getsize(out_path) / 1024 / 1024
        self.stdout.write(self.style.SUCCESS(
            f"Wrote {out_path} ({size_mb:.2f} MB, {len(all_objects)} objects, "
            f"anonymized {len(name_map)} names)"
        ))
