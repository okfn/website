# Staff/Board/Advisory board pages

## Problem

We will have at least three pages where we present people to visitors:

* On the *staff* page
* On the *board* page
* On the *advisory board* page

We need to decide on the attributes for each of these and see if things can be reused between them.

## Reusability

The people attributes can be reused between the pages although there are more attributes associated with a staff member then members of the board or the advisory board:

> My feeling is that these same attributes (minus the unit designations) could
> apply consistently across all of these related 'people' pages in the about
> section: staff, board, advisory board (contact info/email address would not
> be a required field as it's only needed for staff)

This could for example be implemented via inheritance of a Staff member from a Person object (in Django).

## Decision

### Person attributes

Attributes for all persons listed on the website

* name
* title
* bio/description
* email address *(optional)*
* photo

### Staff member attributes

Same attributes as person except that email address is *not optional*. Extra attributes of staff members:

* unit
    * leadership, ltp, network, ops, knowledge, or services
* head of unit
    * boolean
