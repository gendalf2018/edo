
$(document).ready(function(){
  var toolbar = $('.doc-tools');
  var header = $('.header');

  var toolbarTop = toolbar.css('top'),
      toolbarTop = toolbarTop.slice(0, toolbarTop.length - 2),
      toolbarHeight = toolbar.css('height').slice(0, toolbar.css('height').length - 2);

  var winScrollPrevious = 0;
  $(window).scroll(function(){

    var top = toolbar.css('top'),
        top = top.slice(0, top.length - 2);
    if(window.pageYOffset > winScrollPrevious && window.pageYOffset < 100){
      toolbar.css('top', (toolbarTop-window.pageYOffset) +  'px');
    } else if(window.pageYOffset < winScrollPrevious && window.pageYOffset < 100) {
      toolbar.css('top', (100 - window.pageYOffset) + 'px')
    }
    if (window.pageYOffset > 100) {
      toolbar.css('top', '0');
    }
    winScrollPrevious = window.pageYOffset;
  })
  if (window.pageYOffset > 100) {
    toolbar.css('top', '0');
  }

  $('.editor-main').css('margin-top', toolbarHeight + 'px')

  function sendChanges() {
    console.log('changes', documentHasBeenModified)
    if(documentHasBeenModified){
      var docName = jQuery('#doc-name').val();
      var docId = jQuery('#doc_id').val()
      var docString = jQuery(textBox).html();
      jQuery.ajax({
        type: 'POST',
        url: 'http://' + window.location.host + '/history/',
        data: {
          name: docName,
          html: docString,
          doc_id: docId,
        }
      })
    }
  }

  $("#saveToSystem").click(function(){
      var docName = jQuery('#doc-name').val();
      var docId = jQuery('#doc_id').val()
      var docString = jQuery(textBox).html();
      jQuery.ajax({
        type: 'POST',
        url: 'http://' + window.location.host + '/editor/save/',
        data: {
          name: docName,
          html: docString,
          doc_id: docId || null,
        },
        success: function(resp) {
          var alarm = jQuery('.doc-alerting');
          alarm.fadeIn('fast');
          setTimeout(function(){
            alarm.fadeOut();
          }, 1000)
          sendChanges();
          if(newDoc) {
            newDoc = false;
          }
          jQuery('#doc_id').val(resp.doc_id)
          checkDisabled();
        }
      })
  })
  var historyShowing = false;

  $("#showHistoryBtn").click(function(){
    if(!historyShowing){
      $('span[umodified="modified"]').each(function(i, el){
        $(el).addClass('history-added');
        var uid = $(el).attr('moduid');
        var historyEl = $(".history[history-uid=" + uid + "]")[0];
        var color = $(historyEl).attr('history-color');
        $(el).css('border-color', color);
      })
      $('span[umodified="removed"]').each(function(i, el){
        $(el).addClass('history-removed')
        $(el).html('<i class="fas fa-times"></i>')
        var uid = $(el).attr('moduid');
        var historyEl = $(".history[history-uid=" + uid + "]")[0];
        var color = $(historyEl).attr('history-color');
        $(el).css('color', color);
      })
      $(this).addClass('btn-warning');
    } else {
      $('span[umodified="modified"]').each(function(i, el){
        $(el).removeClass('history-added')
      })
      $('span[umodified="removed"]').each(function(i, el){
        $(el).removeClass('history-removed')
        $(el).html('')
      })
      $(this).removeClass('btn-warning');
    }
    historyShowing = !historyShowing
  })

  jQuery(".delete-group").click(function(){
    var el = jQuery(this);
    var gid = el.attr('gid'),
        docid = el.attr('docid');
    jQuery.ajax({
      type: 'DELETE',
      url: 'http://' + window.location.host + '/editor/groups/',
      data: {
        doc: docid,
        group: gid,
      },
      success: function(resp) {
        el.fadeOut('fast', function(){
          el.parent().remove();
        })
      }
    })
  });
  // enables buttons when document is saved
  function checkDisabled() {
    var newDoc = jQuery('#doc_id').val().length === 0 ? true : false;
    console.log("CHECKING", newDoc, 'doc', jQuery('#doc_id').val().length)
    jQuery('button').each(function(){
      var el = jQuery(this);
      console.log('button',el.attr('id'))
      if(!newDoc){
        el.attr('disabled', false)
        if(el.attr('id')==='createNewFile'){
          el.attr('disabled', true)
        }
      } else {
        el.attr('disabled', true);
        if(el.attr('id')==='createNewFile' || el.attr('id')==='saveToSystem'){
          el.attr('disabled', false)
        }
      }
    })
    var inp = jQuery('#loadFile')[0];
    if(!newDoc){
      jQuery(inp).attr('disabled', true)
    } else {
      console.log("NEW")
      jQuery(inp).attr('disabled', false)
    }
  }
  checkDisabled();

})
