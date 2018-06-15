/*
 * jQuery mmenu v5.7.8
 * @requires jQuery 1.7.0 or later
 *
 * mmenu.frebsite.nl
 *	
 * Copyright (c) Fred Heusschen
 * www.frebsite.nl
 *
 * License: CC-BY-NC-4.0
 * http://creativecommons.org/licenses/by-nc/4.0/
 */

(function( $ ) {

	var _PLUGIN_	= 'mmenu',
		_VERSION_	= '5.7.8';


	//	Plugin already excists
	if ( $[ _PLUGIN_ ] && $[ _PLUGIN_ ].version > _VERSION_ )
	{
		return;
	}


	/*
		Class
	*/
	$[ _PLUGIN_ ] = function( $menu, opts, conf )
	{
		this.$menu	= $menu;
		this._api	= [ 'bind', 'getInstance', 'update', 'initPanels', 'openPanel', 'closePanel', 'closeAllPanels', 'setSelected' ];
		this.opts	= opts;
		this.conf	= conf;
		this.vars	= {};
		this.cbck	= {};


		if ( typeof this.___deprecated == 'function' )
		{
			this.___deprecated();
		}


		this._initMenu();
		this._initAnchors();

		var $pnls = this.$pnls.children();
		
		this._initAddons();
		this.initPanels( $pnls );


		if ( typeof this.___debug == 'function' )
		{
			this.___debug();
		}

		return this;
	};

	$[ _PLUGIN_ ].version 	= _VERSION_;
	$[ _PLUGIN_ ].addons 	= {};
	$[ _PLUGIN_ ].uniqueId 	= 0;


	$[ _PLUGIN_ ].defaults 	= {
		extensions		: [],
		initMenu 		: function() {},
		initPanels 		: function() {},
		navbar 			: {
			add 			: true,
			title			: 'Menu',
			titleLink		: 'panel'
		},
		onClick			: {
//			close			: true,
//			preventDefault	: null,
			setSelected		: true
		},
		slidingSubmenus	: true
	};

	$[ _PLUGIN_ ].configuration = {
		classNames			: {
			divider		: 'Divider',
			inset 		: 'Inset',
			panel		: 'Panel',
			selected	: 'Selected',
			spacer		: 'Spacer',
			vertical	: 'Vertical'
		},
		clone				: false,
		openingInterval		: 25,
		panelNodetype		: 'ul, ol, div',
		transitionDuration	: 400
	};

	$[ _PLUGIN_ ].prototype = {

//	TEMP backward compat
init: function( $panels )
{
	this.initPanels( $panels );
},

		getInstance: function()
		{
			return this;
		},

		update: function()
		{
			this.trigger( 'update' );
		},

		initPanels: function( $panels )
		{
			$panels = $panels.not( '.' + _c.nopanel );
			$panels = this._initPanels( $panels );

			this.opts.initPanels.call( this, $panels );

			this.trigger( 'initPanels', $panels );
			this.trigger( 'update' );
		},

		openPanel: function( $panel )
		{
			var $l = $panel.parent(),
				that = this;

			//	Vertical
			if ( $l.hasClass( _c.vertical ) )
			{
				var $sub = $l.parents( '.' + _c.subopened );
				if ( $sub.length )
				{
					this.openPanel( $sub.first() );
					return;
				}
				$l.addClass( _c.opened );

				this.trigger( 'openPanel' 	, $panel );
				this.trigger( 'openingPanel', $panel );
				this.trigger( 'openedPanel'	, $panel );
			}

			//	Horizontal
			else
			{
				if ( $panel.hasClass( _c.current ) )
				{
					return;
				}

				var $panels = this.$pnls.children( '.' + _c.panel ),
					$current = $panels.filter( '.' + _c.current );

				$panels
					.removeClass( _c.highest )
					.removeClass( _c.current )
					.not( $panel )
					.not( $current )
					.not( '.' + _c.vertical )
					.addClass( _c.hidden );

				if ( !$[ _PLUGIN_ ].support.csstransitions )
				{
					$current.addClass( _c.hidden );
				}

				if ( $panel.hasClass( _c.opened ) )
				{
					$panel
						.nextAll( '.' + _c.opened )
						.addClass( _c.highest )
						.removeClass( _c.opened )
						.removeClass( _c.subopened );
				}
				else
				{
					$panel.addClass( _c.highest );
					$current.addClass( _c.subopened );
				}

				$panel
					.removeClass( _c.hidden )
					.addClass( _c.current );

				that.trigger( 'openPanel', $panel );

				//	Without the timeout the animation won't work because the element had display: none;
				setTimeout(
					function()
					{
						$panel
							.removeClass( _c.subopened )
							.addClass( _c.opened );

						that.trigger( 'openingPanel', $panel );

						//	Callback
						that.__transitionend( $panel,
							function()
							{
								that.trigger( 'openedPanel', $panel );
							}, that.conf.transitionDuration
						);

					}, this.conf.openingInterval
				);
			}
		},

		closePanel: function( $panel )
		{
			var $l = $panel.parent();

			//	Vertical only
			if ( $l.hasClass( _c.vertical ) )
			{
				$l.removeClass( _c.opened );

				this.trigger( 'closePanel'	, $panel );
				this.trigger( 'closingPanel', $panel );
				this.trigger( 'closedPanel'	, $panel );
			}
		},

		closeAllPanels: function()
		{
			//	Vertical
			this.$menu
				.find( '.' + _c.listview )
				.children()
				.removeClass( _c.selected )
				.filter( '.' + _c.vertical )
				.removeClass( _c.opened );

			//	Horizontal
			var $pnls = this.$pnls.children( '.' + _c.panel ),
				$frst = $pnls.first();

			this.$pnls
				.children( '.' + _c.panel )
				.not( $frst )
				.removeClass( _c.subopened )
				.removeClass( _c.opened )
				.removeClass( _c.current )
				.removeClass( _c.highest )
				.addClass( _c.hidden );

			this.openPanel( $frst );
		},
		
		togglePanel: function( $panel )
		{
			var $l = $panel.parent();

			//	Vertical only
			if ( $l.hasClass( _c.vertical ) )
			{
				this[ $l.hasClass( _c.opened ) ? 'closePanel' : 'openPanel' ]( $panel );
			}
		},

		setSelected: function( $li )
		{
			this.$menu.find( '.' + _c.listview ).children( '.' + _c.selected ).removeClass( _c.selected );
			$li.addClass( _c.selected );

			this.trigger( 'setSelected', $li );
		},

		bind: function( evnt, fn )
		{

//	TEMP backward compat
evnt = (evnt == 'init') ? 'initPanels' : evnt;

			this.cbck[ evnt ] = this.cbck[ evnt ] || [];
			this.cbck[ evnt ].push( fn );
		},

		trigger: function()
		{
			var that = this,
				args = Array.prototype.slice.call( arguments ),
				evnt = args.shift();

//	TEMP backward compat
evnt = (evnt == 'init') ? 'initPanels' : evnt;

			if ( this.cbck[ evnt ] )
			{
				for ( var e = 0, l = this.cbck[ evnt ].length; e < l; e++ )
                {
                    this.cbck[ evnt ][ e ].apply( that, args );
                }
			}
		},

		_initMenu: function()
		{
			var that = this;

			//	Clone if needed
			if ( this.conf.clone )
			{
				this.$orig = this.$menu;
				this.$menu = this.$orig.clone( true );
				this.$menu.add( this.$menu.find( '[id]' ) )
					.filter( '[id]' )
					.each(
						function()
						{
							$(this).attr( 'id', _c.mm( $(this).attr( 'id' ) ) );
						}
					);
			}

			//	Via options
			this.opts.initMenu.call( this, this.$menu, this.$orig );

			//	Add ID
			this.$menu.attr( 'id', this.$menu.attr( 'id' ) || this.__getUniqueId() );

			//	Add markup
			this.$pnls = $( '<div class="' + _c.panels + '" />' )
				.append( this.$menu.children( this.conf.panelNodetype ) )
				.prependTo( this.$menu );

			//	Add classes
			this.$menu
				.parent()
				.addClass( _c.wrapper );

			var clsn = [ _c.menu ];

			if ( !this.opts.slidingSubmenus )
			{
				clsn.push( _c.vertical );
			}

			//	Add extensions classes
			this.opts.extensions = this.opts.extensions.length ? 'mm-' + this.opts.extensions.join( ' mm-' ) : '';

			if ( this.opts.extensions )
			{
				clsn.push( this.opts.extensions );
			}

			this.$menu.addClass( clsn.join( ' ' ) );

			this.trigger( '_initMenu' );
		},

		_initPanels: function( $panels )
		{
			var that = this;

			var $lists = this.__findAddBack( $panels, 'ul, ol' );

			//	Add List classname
			this.__refactorClass( $lists, this.conf.classNames.inset, 'inset' )
				.addClass( _c.nolistview + ' ' + _c.nopanel );

			$lists.not( '.' + _c.nolistview )
				.addClass( _c.listview );

			var $lis = this.__findAddBack( $panels, '.' + _c.listview ).children();

			//	Refactor classnames
			this.__refactorClass( $lis, this.conf.classNames.selected, 'selected' );
			this.__refactorClass( $lis, this.conf.classNames.divider, 'divider' );
			this.__refactorClass( $lis, this.conf.classNames.spacer, 'spacer' );
			this.__refactorClass( this.__findAddBack( $panels, '.' + this.conf.classNames.panel ), this.conf.classNames.panel, 'panel' );

			//	Create panels
			var $curpanels = $(),
				$oldpanels = $panels
					.add( $panels.find( '.' + _c.panel ) )
					.add( this.__findAddBack( $panels, '.' + _c.listview ).children().children( this.conf.panelNodetype ) )
					.not( '.' + _c.nopanel );

			this.__refactorClass( $oldpanels, this.conf.classNames.vertical, 'vertical' );
			
			if ( !this.opts.slidingSubmenus )
			{
				$oldpanels.addClass( _c.vertical );
			}

			$oldpanels
				.each(
					function()
					{
						var $t = $(this),
							$p = $t;

						if ( $t.is( 'ul, ol' ) )
						{
							$t.wrap( '<div class="' + _c.panel + '" />' );
							$p = $t.parent();
						}
						else
						{
							$p.addClass( _c.panel );
						}

						var id = $t.attr( 'id' );
						$t.removeAttr( 'id' );
						$p.attr( 'id', id || that.__getUniqueId() );

						if ( $t.hasClass( _c.vertical ) )
						{
							$t.removeClass( that.conf.classNames.vertical );
							$p.add( $p.parent() ).addClass( _c.vertical );
						}

						$curpanels = $curpanels.add( $p );
					} 
				);

			var $allpanels = $('.' + _c.panel, this.$menu);

			//	Add open and close links to menu items
			$curpanels
				.each(
					function( i )
					{
						var $t = $(this),
							$p = $t.parent(),
							$a = $p.children( 'a, span' ).first();

						var id, $b;

						if ( !$p.is( '.' + _c.panels ) )
						{
							$p.data( _d.child, $t );
							$t.data( _d.parent, $p );
						}

						//	Open link
						if ( !$p.children( '.' + _c.next ).length )
						{
							if ( $p.parent().is( '.' + _c.listview ) )
							{
								id = $t.attr( 'id' );
								$b = $( '<a class="' + _c.next + '" href="#' + id + '" data-target="#' + id + '" />' ).insertBefore( $a );

								if ( $a.is( 'span' ) )
								{
									$b.addClass( _c.fullsubopen );
								}
							}
						}

						//	Navbar
						if ( $t.children( '.' + _c.navbar ).length ||
							$p.hasClass( _c.vertical )
						) {
							return;
						}

						if ( $p.parent().is( '.' + _c.listview ) )
						{
							//	Listview, the panel wrapping this panel
							$p = $p.closest( '.' + _c.panel );
						}
						else
						{
							//	Non-listview, the first panel that has an anchor that links to this panel
							$a = $p.closest( '.' + _c.panel ).find( 'a[href="#' + $t.attr( 'id' ) + '"]' ).first();
							$p = $a.closest( '.' + _c.panel );
						}
						
						// fix: _url undefined
						var _url = false;
						var $navbar = $( '<div class="' + _c.navbar + '" />' );

						if ( that.opts.navbar.add )
						{
							$t.addClass( _c.hasnavbar );
						}

						if ( $p.length )
						{
							id = $p.attr( 'id' );
							switch ( that.opts.navbar.titleLink )
							{
								case 'anchor':
									_url = $a.attr( 'href' );
									break;

								case 'panel':
								case 'parent':
									_url = '#' + id;
									break;

								default:
									_url = false;
									break;
							}

							$navbar
								.append( '<a class="' + _c.btn + ' ' + _c.prev + '" href="#' + id + '" data-target="#' + id + '" />' )
								.append( $('<a class="' + _c.title + '"' + ( _url ? ' href="' + _url + '"' : '' ) + ' />').text( $a.text() ) )
								.prependTo( $t );
						}
						else if ( that.opts.navbar.title )
						{
							$navbar
								.append( '<a class="' + _c.title + '">' + $[ _PLUGIN_ ].i18n( that.opts.navbar.title ) + '</a>' )
								.prependTo( $t );
						}
					}
				);


			//	Add opened-classes to parents
			var $s = this.__findAddBack( $panels, '.' + _c.listview )
				.children( '.' + _c.selected )
				.removeClass( _c.selected )
				.last()
				.addClass( _c.selected );

			$s.add( $s.parentsUntil( '.' + _c.menu, 'li' ) )
				.filter( '.' + _c.vertical )
				.addClass( _c.opened )
				.end()
				.each(
					function()
					{
						$(this).parentsUntil( '.' + _c.menu, '.' + _c.panel )
							.not( '.' + _c.vertical )
							.first()
							.addClass( _c.opened )
							.parentsUntil( '.' + _c.menu, '.' + _c.panel )
							.not( '.' + _c.vertical )
							.first()
							.addClass( _c.opened )
							.addClass( _c.subopened );
					}
				);


			//	Add opened-classes to child
			$s.children( '.' + _c.panel )
				.not( '.' + _c.vertical )
				.addClass( _c.opened )
				.parentsUntil( '.' + _c.menu, '.' + _c.panel )
				.not( '.' + _c.vertical )
				.first()
				.addClass( _c.opened )
				.addClass( _c.subopened );


			//	Set current opened
			var $current = $allpanels.filter( '.' + _c.opened );
			if ( !$current.length )
			{
				$current = $curpanels.first();
			}
			$current
				.addClass( _c.opened )
				.last()
				.addClass( _c.current );


			//	Rearrange markup
			$curpanels
				.not( '.' + _c.vertical )
				.not( $current.last() )
				.addClass( _c.hidden )
				.end()
				.filter(
					function()
					{
						return !$(this).parent().hasClass( _c.panels  );
					}
				)
				.appendTo( this.$pnls );

			this.trigger( '_initPanels', $curpanels );

			return $curpanels;
		},

		_initAnchors: function()
		{
			var that = this;

			glbl.$body
				.on( _e.click + '-oncanvas',
					'a[href]',
					function( e )
					{
						var $t = $(this),
							fired 	= false,
							inMenu 	= that.$menu.find( $t ).length;

						//	Find behavior for addons
						for ( var a in $[ _PLUGIN_ ].addons )
						{
							if ( $[ _PLUGIN_ ].addons[ a ].clickAnchor.call( that, $t, inMenu ) )
							{
								fired = true;
								break;
							}
						}

						var _h = $t.attr( 'href' );

						//	Open/Close panel
						if ( !fired && inMenu )
						{
							if ( _h.length > 1 && _h.slice( 0, 1 ) == '#' )
							{
								try
								{
									var $h = $(_h, that.$menu);
									if ( $h.is( '.' + _c.panel ) )
									{
										fired = true;
										that[ $t.parent().hasClass( _c.vertical ) ? 'togglePanel' : 'openPanel' ]( $h );
									}
								}
								catch( err ) {}
							}
						}

						if ( fired )
						{
							e.preventDefault();
						}


						//	All other anchors in lists
						if ( !fired && inMenu )
						{
							if ( $t.is( '.' + _c.listview + ' > li > a' ) && !$t.is( '[rel="external"]' ) && !$t.is( '[target="_blank"]' ) )
							{

								//	Set selected item
								if ( that.__valueOrFn( that.opts.onClick.setSelected, $t ) )
								{
									that.setSelected( $(e.target).parent() );
								}
	
								//	Prevent default / don't follow link. Default: false
								var preventDefault = that.__valueOrFn( that.opts.onClick.preventDefault, $t, _h.slice( 0, 1 ) == '#' );
								if ( preventDefault )
								{
									e.preventDefault();
								}

								//	Close menu. Default: true if preventDefault, false otherwise
								if ( that.__valueOrFn( that.opts.onClick.close, $t, preventDefault ) )
								{
									that.close();
								}
							}
						}
					}
				);

			this.trigger( '_initAnchors' );
		},

		_initAddons: function()
		{
			//	Add add-ons to plugin
			var a;
			for ( a in $[ _PLUGIN_ ].addons )
			{
				$[ _PLUGIN_ ].addons[ a ].add.call( this );
				$[ _PLUGIN_ ].addons[ a ].add = function() {};
			}

			//	Setup adds-on for menu
			for ( a in $[ _PLUGIN_ ].addons )
			{
				$[ _PLUGIN_ ].addons[ a ].setup.call( this );
			}

			this.trigger( '_initAddons' );
		},

		_getOriginalMenuId: function()
		{
			var id = this.$menu.attr( 'id' );
			if ( id && id.length )
			{
				if ( this.conf.clone )
				{
					id = _c.umm( id );
				}
			}
			return id;
		},

		__api: function()
		{
			var that = this,
				api = {};

			$.each( this._api, 
				function( i )
				{
					var fn = this;
					api[ fn ] = function()
					{
						var re = that[ fn ].apply( that, arguments );
						return ( typeof re == 'undefined' ) ? api : re;
					};
				}
			);
			return api;
		},

		__valueOrFn: function( o, $e, d )
		{
			if ( typeof o == 'function' )
			{
				return o.call( $e[ 0 ] );
			}
			if ( typeof o == 'undefined' && typeof d != 'undefined' )
			{
				return d;
			}
			return o;
		},

		__refactorClass: function( $e, o, c )
		{
			return $e.filter( '.' + o ).removeClass( o ).addClass( _c[ c ] );
		},

		__findAddBack: function( $e, s )
		{
			return $e.find( s ).add( $e.filter( s ) );
		},

		__filterListItems: function( $i )
		{
			return $i
				.not( '.' + _c.divider )
				.not( '.' + _c.hidden );
		},

		__transitionend: function( $e, fn, duration )
		{
			var _ended = false,
				_fn = function( e )
				{

					if ( typeof e !== 'undefined' )
					{
						if ( $(e.target).is( $e ) )
						{
							$e.unbind( _e.transitionend );
							$e.unbind( _e.webkitTransitionEnd );
						}
						else
						{
							return false;
						}
					}

					if ( !_ended )
					{
						fn.call( $e[ 0 ] );
					}
					_ended = true;
				};
	
			$e.on( _e.transitionend, _fn );
			$e.on( _e.webkitTransitionEnd, _fn );
			setTimeout( _fn, duration * 1.1 );
		},
		
		__getUniqueId: function()
		{
			return _c.mm( $[ _PLUGIN_ ].uniqueId++ );
		}
	};


	/*
		jQuery plugin
	*/
	$.fn[ _PLUGIN_ ] = function( opts, conf )
	{
		//	First time plugin is fired
		initPlugin();

		//	Extend options
		opts = $.extend( true, {}, $[ _PLUGIN_ ].defaults, opts );
		conf = $.extend( true, {}, $[ _PLUGIN_ ].configuration, conf );

		var $result = $();
		this.each(
			function()
			{
				var $menu = $(this);
				if ( $menu.data( _PLUGIN_ ) )
				{
					return;
				}

				var _menu = new $[ _PLUGIN_ ]( $menu, opts, conf );
				_menu.$menu.data( _PLUGIN_, _menu.__api() );

				$result = $result.add( _menu.$menu );
			}
		);

		return $result;
	};


	/*
		I18N
	*/
	$[ _PLUGIN_ ].i18n = (function() {

		var trns = {};

		return function( t )
		{
			switch( typeof t )
			{
				case 'object':
					$.extend( trns, t );
					return trns;
					break;

				case 'string':
					return trns[ t ] || t;
					break;

				case 'undefined':
				default:
					return trns;
					break;
			}
		};
	})();


	/*
		SUPPORT
	*/
	$[ _PLUGIN_ ].support = {
		touch: 'ontouchstart' in window || navigator.msMaxTouchPoints || false,
		csstransitions: (function()
		{
			//	Use Modernizr test
			if ( typeof Modernizr !== 'undefined' &&
				 typeof Modernizr.csstransitions !== 'undefined'
			) {
				return Modernizr.csstransitions;
			}

			var b = document.body || document.documentElement,
				s = b.style,
				p = 'transition';

			//	Default support
			if ( typeof s[ p ] == 'string' )
			{
				return true;
			}

			//	Vendor specific support
			var v = [ 'Moz', 'webkit', 'Webkit', 'Khtml', 'O', 'ms' ];
			p = p.charAt( 0 ).toUpperCase() + p.substr( 1 );

			for ( var i = 0; i < v.length; i++ )
			{
				if ( typeof s[ v[ i ] + p ] == 'string' )
				{
					return true;
				}
			}

			//	No support
			return false;
		})(),
		csstransforms: (function() {
			if ( typeof Modernizr !== 'undefined' &&
				 typeof Modernizr.csstransforms !== 'undefined'
			) {
				return Modernizr.csstransforms;
			}

			//	w/o Modernizr, we'll assume you only support modern browsers :/
			return true;
		})(),
		csstransforms3d: (function() {
			if ( typeof Modernizr !== 'undefined' &&
				 typeof Modernizr.csstransforms3d !== 'undefined'
			) {
				return Modernizr.csstransforms3d;
			}

			//	w/o Modernizr, we'll assume you only support modern browsers :/
			return true;
		})()
	};


	//	Global variables
	var _c, _d, _e, glbl;

	function initPlugin()
	{
		if ( $[ _PLUGIN_ ].glbl )
		{
			return;
		}

		glbl = {
			$wndw : $(window),
			$docu : $(document),
			$html : $('html'),
			$body : $('body')
		};


		//	Classnames, Datanames, Eventnames
		_c = {};
		_d = {};
		_e = {};

		$.each( [ _c, _d, _e ],
			function( i, o )
			{
				o.add = function( a )
				{
					a = a.split( ' ' );
					for ( var b = 0, l = a.length; b < l; b++ )
					{
						o[ a[ b ] ] = o.mm( a[ b ] );
					}
				};
			}
		);

		//	Classnames
		_c.mm = function( c ) { return 'mm-' + c; };
		_c.add( 'wrapper menu panels panel nopanel current highest opened subopened navbar hasnavbar title btn prev next listview nolistview inset vertical selected divider spacer hidden fullsubopen' );
		_c.umm = function( c )
		{
			if ( c.slice( 0, 3 ) == 'mm-' )
			{
				c = c.slice( 3 );
			}
			return c;
		};

		//	Datanames
		_d.mm = function( d ) { return 'mm-' + d; };
		_d.add( 'parent child' );

		//	Eventnames
		_e.mm = function( e ) { return e + '.mm'; };
		_e.add( 'transitionend webkitTransitionEnd click scroll keydown mousedown mouseup touchstart touchmove touchend orientationchange' );


		$[ _PLUGIN_ ]._c = _c;
		$[ _PLUGIN_ ]._d = _d;
		$[ _PLUGIN_ ]._e = _e;

		$[ _PLUGIN_ ].glbl = glbl;
	}


})( jQuery );
