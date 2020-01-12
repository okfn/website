$(document).ready(function() {
  // menus
  $("#mmenu").mmenu({
     // options
     searchfield: true,
     extensions: [
       "position-right",
       "theme-dark"
     ]
  }, {
     // configuration
     classNames: {
       selected: "active"
     }
  });
  $("#side-nav").mmenu({
     // options
     offCanvas: false,
     autoHeight: true
  }, {
     // configuration
     classNames: {
       selected: "active"
     }
  });


  // show / hide search bar
  $('#display-search-bar').on('click', function () {
      $('#main-search-bar').addClass("active");
  });
  $('#main-search-bar .cancel').on('click', function (event) {
      event.preventDefault();
      $('#main-search-bar').removeClass("active");
  });


  // external links
  $('a[rel*=external]').click(function () {
      window.open(this.href);
      return false;
  });


  // home video
  // Need to manipulate what aldryn-video gives us
  var homeVideo = $('body.home-template .embed-responsive');
  var homeVideoIframe = $(homeVideo).children("iframe");
  // add some attributes
  $(homeVideo).attr('id', 'video');
  $(homeVideoIframe).attr('allow', 'autoplay');
  // edit the params
  var framesrc = $(homeVideoIframe).attr('src');
  if (framesrc) {
    var newframesrc = framesrc.replace('feature=oembed', 'enablejsapi=1');
    $(homeVideoIframe).attr('src', newframesrc);
  }

  // Show video and play it
  $('#play-home-video').on('click', function () {
    $('#page').addClass("video-active");
    callPlayer('video', 'playVideo');
  });

  // Stop video and hide it
  $('#close-home-video').on('click', function () {
    callPlayer('video', 'stopVideo');
    $('#page').removeClass("video-active");
  });

});

/**
 * @author       Rob W <gwnRob@gmail.com>
 * @website      https://stackoverflow.com/a/7513356/938089
 * @version      20190409
 * @description  Executes function on a framed YouTube video (see website link)
 *               For a full list of possible functions, see:
 *               https://developers.google.com/youtube/js_api_reference
 * @param String frame_id The id of (the div containing) the frame
 * @param String func     Desired function to call, eg. "playVideo"
 *        (Function)      Function to call when the player is ready.
 * @param Array  args     (optional) List of arguments to pass to function func*/
function callPlayer(frame_id, func, args) {
    if (window.jQuery && frame_id instanceof jQuery) frame_id = frame_id.get(0).id;
    var iframe = document.getElementById(frame_id);
    if (iframe && iframe.tagName.toUpperCase() != 'IFRAME') {
        iframe = iframe.getElementsByTagName('iframe')[0];
    }

    // When the player is not ready yet, add the event to a queue
    // Each frame_id is associated with an own queue.
    // Each queue has three possible states:
    //  undefined = uninitialised / array = queue / 0 = ready
    if (!callPlayer.queue) callPlayer.queue = {};
    var queue = callPlayer.queue[frame_id],
        domReady = document.readyState == 'complete';

    if (domReady && !iframe) {
        // DOM is ready and iframe does not exist. Log a message
        window.console && console.log('callPlayer: Frame not found; id=' + frame_id);
        if (queue) clearInterval(queue.poller);
    } else if (func === 'listening') {
        // Sending the "listener" message to the frame, to request status updates
        if (iframe && iframe.contentWindow) {
            func = '{"event":"listening","id":' + JSON.stringify(''+frame_id) + '}';
            iframe.contentWindow.postMessage(func, '*');
        }
    } else if ((!queue || !queue.ready) && (
               !domReady ||
               iframe && !iframe.contentWindow ||
               typeof func === 'function')) {
        if (!queue) queue = callPlayer.queue[frame_id] = [];
        queue.push([func, args]);
        if (!('poller' in queue)) {
            // keep polling until the document and frame is ready
            queue.poller = setInterval(function() {
                callPlayer(frame_id, 'listening');
            }, 250);
            // Add a global "message" event listener, to catch status updates:
            messageEvent(1, function runOnceReady(e) {
                    if (!iframe) {
                        iframe = document.getElementById(frame_id);
                        if (!iframe) return;
                        if (iframe.tagName.toUpperCase() != 'IFRAME') {
                            iframe = iframe.getElementsByTagName('iframe')[0];
                            if (!iframe) return;
                        }
                    }
                if (e.source === iframe.contentWindow) {
                    // Assume that the player is ready if we receive a
                    // message from the iframe
                    clearInterval(queue.poller);
                    queue.ready = true;
                    messageEvent(0, runOnceReady);
                    // .. and release the queue:
                    while (tmp = queue.shift()) {
                        callPlayer(frame_id, tmp[0], tmp[1]);
                    }
                }
            }, false);
        }
    } else if (iframe && iframe.contentWindow) {
        // When a function is supplied, just call it (like "onYouTubePlayerReady")
        if (func.call) return func();
        // Frame exists, send message
        iframe.contentWindow.postMessage(JSON.stringify({
            "event": "command",
            "func": func,
            "args": args || [],
            "id": frame_id
        }), "*");
    }
    /* IE8 does not support addEventListener... */
    function messageEvent(add, listener) {
        var w3 = add ? window.addEventListener : window.removeEventListener;
        w3 ?
            w3('message', listener, !1)
        :
            (add ? window.attachEvent : window.detachEvent)('onmessage', listener);
    }
}
