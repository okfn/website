# Technical approach

## Problem

Decide on the best technical approach to run our new site.

In parallel with discussions (what to save from the old version of the website and the new sitemap) about what the content and information architecture of the new site should be we started discussing options for creating, managing, hosting and operating the new okfn.org.

In what follows, our discussion should be driven by the following concerns, in rough order of priority. Please also feel free to question these items and their relative priority:

1. The ease with which we will be able to adapt the chosen technologies to our *external* user's needs (navigation, searchability, responsiveness of layout, performance) [**USER**]
2. The ease with which the site content can be maintained and updated *over the long term* by OKF central staff with varying degrees of technical interest or skill. [**CONT**]
3. The ease with which technical staff can update and maintain layout templates and styles, and adapt these to changes in browser technology or device usage. [**DSGN**]
4. The amount of up-front effort required to duplicate the (needed) functionality of the existing [okfn.org](http://okfn.org/). [**EFFT**]
5. The breadth and quality of the existing community surrounding the chosen technologies. [**CMTY**]
6. The quality and stability of the the technology in question, including evidence of QA and automated testing. [**QUAL**]
7. The ease with which can develop custom features if necessary and integrate them with the site (e.g. a jobs page, events listings, etc.) [**CSTM**]
8. The ease with which we can deploy the site. This includes considerations such as asset pipeline management, integration with external storage (S3) and a CDN, where appropriate, and the ease of managing a staging environment [**DPLY**]

### Comments

One thing to stress here is that given the size and distributed nature of our organisation, the ability to audit what changes were made by who and when, plays an important part in both **CONT** and **DSGN**. The current state of WordPress is largely unauditable, and there isn't a clear division between what lives in the database and what lives in the code.

IMO, content and only content should live in the database. Templates, stylesheets, etc., should *all* live in one version-controlled repository, ideally with few or no external dependencies.

## Decision matrix

| Option name              | USER | CONT | DSGN | EFFT | CMTY | QUAL | CSTM | DPLY | Total | 
| -----------------------  | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :---- | 
| WordPress (blogfarm)     | 2    | 1    | 0    | 5    | 3    | 3    | 1    | 1    | 16    |
| WordPress (new install)  | 3    | 2    | 1    | 4    | 3    | 3    | 1    | 1    | 18    |
| Django (custom)          | 5    | 4    | 5    | 0    | 1    | 3    | 3    | 3    | 24    |
| Django ([django-cms][1]) | 5    | 4    | 4    | 2    | 2    | 3    | 3    | 3    | 26    | 
| [Drupal][6]              | 5    | 4    | 3    | 3    | 3    | 3    | 2    | 1    | 24    |
| [Mezzanine][2]           | 4    | 2    | 2    | 2    | 1    | 3    | 1    | 3    | 18    |
| [fork-cms][3]            |      |      |      |      |      |      |      |      | ?     |
| [concrete5][4]           |      |      |      |      |      |      |      |      | ?     |
| [plone][5]               |      |      |      |      |      |      |      |      | ?     |

USER, CONT, DSGN, EFFT, are scored from 0 to 5. CMTY, QUAL, CSTM, DPLY are scored from 0 to 3. A higher score is better in all categories. All scores are bound to be partially subjective.

[1]: http://django-cms.readthedocs.org/en/develop/
[2]: http://mezzanine.jupo.org/
[3]: http://www.fork-cms.com/
[4]: http://www.concrete5.org/
[5]: https://plone.org/products
[6]: https://drupal.org/

### Basic Django application

Playground for a very basic Django application (using [`django.contrib.flatpages`](https://docs.djangoproject.com/en/dev/ref/contrib/flatpages/):

| Page | URL  |
| :--------- | :--------- |
| Home page | https://radiant-escarpment-7180.herokuapp.com/ |
| About page (dynamic) | https://radiant-escarpment-7180.herokuapp.com/about/ |
| Admin login | https://radiant-escarpment-7180.herokuapp.com/admin/ |
| Admin manage flatpages | https://radiant-escarpment-7180.herokuapp.com/admin/flatpages/flatpage/ |

User/pass: admin/password.

#### Pros

- Simple
- Easily deployable

#### Cons

- Lots of work to do to make this staff friendly: no draft preview, no markdown or WYSIWYG content editing.
- Would be starting from scratch with templates/styles.

### Django-CMS based solution

Playground for a `django-cms` site:

| Page | URL |
| :-- | :-- |
| Home page | https://nameless-refuge-5960.herokuapp.com/ |
| Home page (editable) | https://nameless-refuge-5960.herokuapp.com/?edit |
| Admin login | https://nameless-refuge-5960.herokuapp.com/admin/ |
| Admin pages overview | https://nameless-refuge-5960.herokuapp.com/admin/cms/page/ |

User/pass: admin/password.

#### Pros

- Definitely more of a CMS: the straightforward integration with Django templates is very nice -- placeholders in normal web app templates.
- Nothing binds us to particular underlying templates. Unlike many other CMSes, we have complete control over what HTML is rendered.
- Easy to integrate with anything custom, as underneath it's just a normal Django application.
- Realistically, the underlying framework being Python is a big plus, because it means more meaningful engagement from already-employed OKF technical staff. (To be clear, my personal position is that in an ideal world, language would be a factor for itself, but if we're being pragmatic, absence of ample PHP experience in-house limits our ability to actually build out and modify PHP-based systems.)
- Django-reversion support (versioned pages) out of the box

#### Cons

- django-cms 3.0.0 not out yet, current develop branch has some problems (broken javascript, broken dependency specs)
- Would be starting from scratch with templates/styles.

#### Questions

- Can placeholder content be inherited by child pages?
- How soon until django-cms 3.0.0 is released properly

### Mezzanine based solution

Notes on mezzanine:

#### Pros

- Django-based -- we have Python expertise in-house.
- Stable release

#### Cons

- Not a Django "app", but a project, which is quite messy, and makes integrating our own code more ugly than it should be.
- More "magic" than django-CMS. Default templates, much like Wordpress, make it harder to understand relationships between content and display.
- Draft system not integrated with the content hierarchy.

### Other solutions

Other solutions were not considered in as much detail although some were given some ratings in the decision matrix with an in-depth evaluation. The reason for cutting the evaluation short is time:

> At this stage I'm going to cut short the research phase because 
> I think we have a clear candidate for development in the form of
> django + django-cms. We have limited time to get this stuff done
> so I'm going to proceed on this basis.

## Decision

We will use **Django + Django-CMS**.