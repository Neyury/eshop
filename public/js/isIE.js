
// IE 10 only CSS properties
var ie10Styles = [
    'msTouchAction',
    'msWrapFlow',
    'msWrapMargin',
    'msWrapThrough',
    'msOverflowStyle',
    'msScrollChaining',
    'msScrollLimit',
    'msScrollLimitXMin',
    'msScrollLimitYMin',
    'msScrollLimitXMax',
    'msScrollLimitYMax',
    'msScrollRails',
    'msScrollSnapPointsX',
    'msScrollSnapPointsY',
    'msScrollSnapType',
    'msScrollSnapX',
    'msScrollSnapY',
    'msScrollTranslation',
    'msFlexbox',
    'msFlex',
    'msFlexOrder'];

var ie11Styles = [
    'msTextCombineHorizontal'];

/*
 * Test all IE only CSS properties
 */

var s = document.body.style;
var ieVersion = null;
var property;

// Test IE10 properties
for (var i = 0; i < ie10Styles.length; i++) {
    property = ie10Styles[i];

    if (s[property] != undefined) {
        ieVersion = "ie10";
    }
}

// Test IE11 properties
for (var i = 0; i < ie11Styles.length; i++) {
    property = ie11Styles[i];

    if (s[property] != undefined) {
        ieVersion = "ie11";
    }
}

if (ieVersion) {
  document.body.style.display ="block";

  var tab = document.getElementsByClassName('tab');
  if (tab.length > 0) {
    var div = document.createElement("div");
    div.classList.add("page-message");
    div.innerHTML = "Эта страница может отображаться <b>неправильно</b> в браузере <b>Internet Explorer</b>, воспользуйтесь другим браузером."
    // var main = document.body.querySelector(".main");
    main.insertBefore(div, main.firstChild);

  }
}
