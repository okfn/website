## Getting Started

This plugin requires jquery


As mentioned, creating the menu is really easy. First include jQuery and the jQuery.mmenu-plugin files in your webpage:

```html
<head>
   <script type="text/javascript" language="javascript" src="jquery.js"></script>
   <script type="text/javascript" language="javascript" src="jquery.mmenu.js"></script>
   <link type="text/css" rel="stylesheet" media="all" href="mmenu.css" />
</head>
```
Setup your menu like you normally would, create an UL with nested UL's inside a NAV.
Follow [this tutorial](http://mmenu.frebsite.nl/mmenu-2.2.3/docs/tutorial/page.html) to learn how to setup the HTML.

Now all you need to do, is fire the plugin onDocumentReady:

```js
$("#nav").mmenu({
   // options go here...
});
```

To find out more information about this plugin, please visit the [frebsite.nl](http://mmenu.frebsite.nl/)