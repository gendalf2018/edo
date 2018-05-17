var oDoc, sDefTxt;
var futurePageHeight;
var disallowModify = false;
var documentHasBeenModified = false;
var newDoc = jQuery('#doc_id').val() ? true : false;
function initDoc() {
  oDoc = document.getElementById("textBox");
  sDefTxt = oDoc.innerHTML;
  // if (document.compForm.switchMode.checked) { setDocMode(true); }
}

function formatDoc(sCmd, sValue) {
  if (validateMode()) {
    document.execCommand(sCmd, false, sValue);
    // oDoc.focus();
  }
}

function validateMode() {
  if (!document.compForm.switchMode.checked) { return true ; }
  alert("Uncheck \"Show HTML\". \n Уберите галочку с переключателя Показать HTML");
  // oDoc.focus();
  return false;
}

function setDocMode(bToSource) {
  var oContent;
  if (bToSource) {
    oContent = document.createTextNode(oDoc.innerHTML);
    oDoc.innerHTML = "";
    var oPre = document.createElement("pre");
    oDoc.contentEditable = false;
    oPre.id = "sourceText";
    oPre.contentEditable = true;
    oPre.appendChild(oContent);
    oDoc.appendChild(oPre);
    document.execCommand("defaultParagraphSeparator", false, "div");
  } else {
    if (document.all) {
      oDoc.innerHTML = oDoc.innerText;
    } else {
      oContent = document.createRange();
      oContent.selectNodeContents(oDoc.firstChild);
      oDoc.innerHTML = oContent.toString();
    }
    oDoc.contentEditable = true;
  }
  // oDoc.focus();
}

function printDoc() {
  if (!validateMode()) { return; }
  var oPrntWin = window.open("","_blank","width=450,height=470,left=400,top=100,menubar=yes,toolbar=no,location=no,scrollbars=yes");
  oPrntWin.document.open();
  oPrntWin.document.write("<!doctype html><html><head><title>Print<\/title><\/head><body onload=\"print();\">" + oDoc.innerHTML + "<\/body><\/html>");
  oPrntWin.document.close();
}
window.docEdits = {
    setBackground: function() {
      formatDoc('backcolor',this[this.selectedIndex].value);
      this.selectedIndex=0;
    },
    setPadding: function() {
      var doc = document.querySelector("#A").querySelector('section')
      doc.style.padding = this[this.selectedIndex].value;
      this.selectedIndex=0;
    }
  }
/////////////////////////////////


function createPage(css, width) {
  var page = document.createElement('section');
  page.style.cssText = css;
  page.style.width = width + 'px';
  page.style.minHeight = '0';
  page.style.marginBottom = '10px';
  page.style.border = '1px solid #e2e2e2';
  var paragraph = document.createElement('p');
  var sp = document.createElement('span')
  paragraph.appendChild(sp);
  page.appendChild(paragraph)
  textBox.querySelector("#A").appendChild(page)
  return page
}

function rearrangeContent(pages) {
  for (var i = 0; i < pages.length; i++) {
    var pageChilds = pages[i].childNodes;
    var pageStyle = pages[i].style.cssText;
    var nextPage = pages[i+1];
    var wrongHeight = true;
    while(wrongHeight) {
        if(pages[i].offsetHeight <= futurePageHeight + 10){
          wrongHeight = false;
          break;
        }
        if(!nextPage) {
          nextPage = createPage(pageStyle, pages[i].offsetWidth)
          nextPage.style.minHeight = futurePageHeight + 'px';
          // nextPage.focus();
        }
        var clone = pageChilds[pageChilds.length-1].cloneNode(true);
        nextPage.prepend(clone);
        pageChilds[pageChilds.length-1].remove();
    }
  }
}

function onRemove(e, uid) {
  if(newDoc) return;
  // sendChanges();
  documentHasBeenModified = true;
  var sel = document.getSelection();
  var spn = document.createElement('span');
  spn.setAttribute('umodified', 'removed');
  spn.setAttribute('moduid', uid);
  spn.setAttribute('modtime', new Date().getTime());
  spn.style.display = 'none';
  var range = sel.getRangeAt(0);
  range.insertNode(spn);

  var newRange = document.createRange();
  newRange.setStartBefore(spn, 0);
  newRange.setEndBefore(spn, 0);
  // sel.collapse(spn, true);
}

function onModified(e, uid) {
  if(newDoc) return;
  if(disallowModify) return;
  var parent = e.target.parentNode;
  var pName = parent.nodeName;
  if(e.prevValue.length >= e.newValue.length) {
    return;
  }
  // sendChanges();
  documentHasBeenModified = true;
  // Modifying
  var val;
  for(var i = 0; i< e.newValue.length; i++) {
    if(e.newValue[i] != e.prevValue[i]){
      val = e.newValue[i]
      break;
    }
  }

  if(pName!='SECTION' && pName!='BR' && pName!='DIV'){
    if(!parent.getAttribute('umodified') || parent.getAttribute('moduid') != uid){
      console.log(parent.innerHTML)
      var sel = document.getSelection();
      var range = sel.getRangeAt(0);
      console.log(range)
      if(!range.collapsed) {
        return;
      }
      // formatDoc('undo')

      var spn = document.createElement('span');
      spn.setAttribute('umodified', 'modified');
      spn.setAttribute('moduid', uid);
      spn.setAttribute('modtime', new Date().getTime());
      spn.innerHTML = ' ';
      console.log(range)
      range.insertNode(spn);

      var newRange = document.createRange();
      newRange.setStart(spn, 0);
      newRange.setEnd(spn, 1);
      // sel.collapse(spn, true);
      // spn.innerHTML = '';

    }
  }
  disallowModify = true;
  setTimeout(function(){
    disallowModify = false;
  }.bind(this), 200)

}

function pageWatcher(e) {

  user_id = document.querySelector("#user_id").value;
  var divA = textBox.querySelector("#A");
  // console.log($(textBox).find("#A").length)
  if(!$(textBox).find("#A").length) {
    createNew();
    return;
  }
  var sections = divA.querySelectorAll('section');
  for (var i = 0; i < sections.length; i++) {
    if(sections[i].offsetHeight > futurePageHeight) {
      rearrangeContent(Array.prototype.slice.call(sections, i, sections.length));
    }
  }
  if(e.type === 'DOMCharacterDataModified'){
      onModified(e, user_id);
  }
  if(e.type === 'input' && (e.inputType === 'deleteContentBackward' || e.inputType === 'deleteContentForward')){
    onRemove(e, user_id)
  }
}

function pageDivider(section){
  var children = section.childNodes;
  var sectionCss = section.style.cssText;
  var pageWidth = section.offsetWidth;
  futurePageHeight = pageWidth * 1.414;

  textBox.style.width = pageWidth + 'px';
  textBox.querySelector("#A").style.paddingTop = '0';
  var pageCount = section.clientHeight / futurePageHeight,
      pages = [];
  if(pageCount != Math.round(pageCount)) {
    pageCount = Math.round(pageCount) + 1
  }
  for ( var i = 0; i < pageCount; i++ ) {
    var elArray = [];
    var page = createPage(sectionCss, pageWidth, futurePageHeight);
    for(var item = 0; item < children.length; item ++) {
      var clone = children[item].cloneNode(true);
      if(!(page.offsetHeight + children[item].offsetHeight >= futurePageHeight)) {
          page.appendChild(clone)
      } else {
        children = Array.prototype.slice.call(children, item, children.length);
        break;
      }
      // console.log('height', page.offsetHeight)
    }
    page.style.minHeight = futurePageHeight + 'px'
  }
}

function docxtostring(input){
  require("docx2html")(input.files[0]).then(function(converted){
    var textBox = document.querySelector('#textBox');
    textBox.innerHTML=converted.toString();
    textBox.style.display = "block"
    textBox.querySelector('#A').style.display = 'block'
    window.textBox = textBox;
    var innerDoc = textBox.querySelector('#A').querySelector('section');
    pageDivider(innerDoc)  // section tag
    // pageWatcher(textBox)
    innerDoc.remove();
    textBox.addEventListener('input', pageWatcher, true);
    // textBox.addEventListener("DOMNodeInserted", pageWatcher, true);
    // textBox.addEventListener("DOMNodeRemoved", pageWatcher, true);
    textBox.addEventListener("DOMCharacterDataModified", pageWatcher, true);
    // textBox.addEventListener("selectionchange", pageWatcher, true)
    // innerDoc.style.display = 'none'
  })
}
/////////////////////////////////////
function saveit(){
  console.log('saving')
  var sections = textBox.querySelector('#A').childNodes;
  var styles = [];
  for (var s = 0; s< sections.length; s++) {
    styles.push(sections[s].style.cssText);
    sections[s].style.marginBottom = '0';
    sections[s].style.border = 'none';
  }
  var content = textBox.innerHTML
  var converted = htmlDocx.asBlob(content);
  saveAs(converted, 'test.docx');
  for(var p = 0; p < sections.length; p++) {
    sections[p].style.cssText = styles[p]
  }
}
/////////////////////////////////
function createNew(loaded){
  var textBox = document.querySelector("#textBox");
  if (loaded) {
    textBox.style.display = 'block';
    var divA = textBox.querySelector("#A"),
        section = divA.querySelector('section'),
        width = section.offsetWidth;
        textBox.style.width = width;

  }
  var editableDiv = $("<div id='A' style='background-color: transparent; min-height: 1000px; width: 100%; padding-top: 0px; overflow: auto; display: block;'></div>");
  $(textBox).append(editableDiv);
  var pageCss = "width: 793px; background-color: white; min-height: 1121.3px; padding: 94px; margin-bottom: 10px; border: 1px solid rgb(226, 226, 226);"
  var page = createPage(pageCss, 793);
  page.style.minHeight = (793*1.414) + 'px'
  textBox.style.display = "block";
  textBox.style.width = 793 + 'px';
  textBox.addEventListener('input', pageWatcher, true);
  // textBox.addEventListener("DOMNodeInserted", pageWatcher, true);
  // textBox.addEventListener("DOMNodeRemoved", pageWatcher, true);
  textBox.addEventListener("DOMCharacterDataModified", pageWatcher, true);
  // textBox.addEventListener("selectionchange", pageWatcher, true)
}
