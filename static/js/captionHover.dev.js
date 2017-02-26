

(function($) {

    $.fn.captionHover = function( options ) {

        var settings = $.extend({}, options);

        return this.each( function() {
		    $(this).addClass( 'effect-' + settings.fx );

		    if ( settings.figWidth ) {
		    	$(this).width( settings.figWidth );
		    }

		    if ( settings.figHeight ) {
		    	$(this).width( settings.figHeight );
		    }

		    if ( settings.headColor ) {
		        $(this).find('h2').css( 'color', settings.headColor );
		    }

		    if ( settings.captionColor ) {
		        $(this).find('p').css( 'color', settings.captionColor );
		    }

		    if ( settings.overlay ) {
		        $(this).css( 'background', settings.overlay );
		    }

		    if ( settings.bgCaption ) {
		        $(this).find('figcaption').css( 'background', settings.bgCaption );
		    }

		    if (settings.iconColor ) {
		    	$(this).find('.icon-links a').css('color', settings.iconColor );
		    }
		});
    }

}(jQuery));