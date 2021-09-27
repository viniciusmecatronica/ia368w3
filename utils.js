// search an object inside a iframe and returns the corresponding DOM node


function findHtmlObject(loc, frameId, objId) {
   var oid = null;
// return findHtmlObjectRec(loc, frameId, objId, oid);
   try {
      // IE crashes on recursive call
      return(top.document.frames[frameId].document.getElementById(objId));
   } catch(e) {
      return findHtmlObjectRec(loc, frameId, objId, oid);
      }
}

function findHtmlObjectRec(loc, frameId, objId, oid) {
    // get all iframes in this location
    var elem = loc.getElementsByTagName("iframe");
    var i = 0;
    // for each iframe, seach object
    for(i = 0; i < elem.length; i++) {
      if(oid != null) return oid;    // already found in a recursive call
      if(elem[i].id == frameId && 
        (oid = elem[i].contentDocument.getElementById(objId))) return(oid);
      // try frame within frame
      else oid = findHtmlObjectRec(elem[i].contentDocument, frameId, objId, oid);
    }
    return oid;
}

function readCookie(name) {
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i < ca.length;i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	return null;
}


function createRequest() {
  var ajaxRequest = null;
  try {
      // Opera 8.0+, Firefox, Safari
      ajaxRequest = new XMLHttpRequest();
  } catch (e) {
   // Internet Explorer Browsers
   try {
       ajaxRequest = new ActiveXObject("Msxml2.XMLHTTP");
   } catch (e) {
      try {
          ajaxRequest = new ActiveXObject("Microsoft.XMLHTTP");
      } catch (e) {
        // Something went wrong
         alert("Navegador no suporta AJAX");
         return null;
       }
    }
  }
  return ajaxRequest;
}



