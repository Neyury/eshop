"use strict";

document.addEventListener("click", documentClickHandler);
document.addEventListener("scroll", initFixedBlocks);

initGallery();
initTabs();
initAnchor();
initColorPalette();
initFilterAmount();
initFilterRange();
initFilterClear();
initShelf();

function documentClickHandler(event) {

  var target = event.target;
  var elements = document.querySelectorAll(".open");


  while (target != this) {
    if(!target) return;
    if (target.classList.contains("open")) {
      target.classList.add("saveopen");
    }
    target = target.parentNode;
  }

  for (var i = 0; i < elements.length; i++) {
    if (!elements[i].classList.contains("saveopen")) {
      elements[i].classList.remove("open");
    }
  }

  for (var i = 0; i < elements.length; i++) {
    if (elements[i].classList.contains("saveopen")) {
      elements[i].classList.remove("saveopen");
    }
  }
}

function toggleThis(event, n, className) {
  var target = event.currentTarget;
  className = className || "open";

  for (var i = 0; i < n - 1; i++) {
    target = target.parentNode;
  }

  target.classList.toggle(className);

  return target;
}

function initTabs() {
  var nav_tabs = document.querySelector(".nav-tabs");
  if (!nav_tabs) return;
  var children = nav_tabs.children;
  var tabs = document.querySelectorAll(".tab");
  var tabs_nav = document.querySelectorAll(".tab-nav");

  if(!children) return;

  if (children){
    for (var i = 0; i < children.length; i++) {
      children[i].addEventListener("click", toggleTab)
    }
  } else return;

  function toggleTab(event) {
    var btn = event.currentTarget;
    window.location.hash = btn.dataset.openTab;

    openTab(btn.dataset.openTab);
    openNav(btn.dataset.openTab);

    for (var i = 0; i < children.length; i++) {
      children[i].classList.remove("active");
    }
    btn.classList.add("active");
  }

  function openTab(hash) {
    for (var i = 0; i < tabs.length; i++) {
      if (tabs[i].dataset.openHash == hash) {
        tabs[i].classList.add("active");
      } else {
        tabs[i].classList.remove("active");
      }
    }
  }

  function openNav(hash) {
    for (var i = 0; i < tabs_nav.length; i++) {
      if (tabs_nav[i].dataset.openHash == hash) {
        tabs_nav[i].classList.add("active");
      } else {
        tabs_nav[i].classList.remove("active");
      }
    }
  }

  if (window.location.hash) {
    var not_valid = true;
    for (var i = 0; i < children.length; i++) {
      if(children[i].dataset.openTab == window.location.hash){
        children[i].classList.add("active");
        openTab(window.location.hash);
        openNav(window.location.hash);
        not_valid = false;
      }
    }
  } else {
    window.location.hash = children[0].dataset.openTab;
    children[0].classList.add("active");
    openTab(children[0].dataset.openTab);
    openNav(children[0].dataset.openTab);
  }
  if (not_valid) {
    window.location.hash = children[0].dataset.openTab;
    children[0].classList.add("active");
    openTab(children[0].dataset.openTab);
    openNav(children[0].dataset.openTab);
  }
}

function initAnchor() {
  var scrollers = document.querySelectorAll(".scroll-to");

  if (scrollers) {
    for (var i = 0; i < scrollers.length; i++) {
      scrollers[i].addEventListener("click", scrollTo);
    }
  } else return 0;


  function scrollTo(event) {
    var scroller = event.currentTarget;
    var target = document.getElementById(scroller.dataset.scrollTo);
    target.scrollIntoView();
  }
}

function initGallery() {
  var gallery = document.getElementById("gallery");
  if (!gallery) return;
  var imageFullContainer = gallery.querySelector(".image-full");
  var imageFull = imageFullContainer.firstElementChild;
  var imageList = gallery.querySelector(".image-list");
  var imageZoom = gallery.querySelector(".image-zoom");
  var imageZone = gallery.querySelector(".image-zoom-zone");
  var imageFade = gallery.querySelector(".image-zoom-fade");
  var ul = imageList.firstElementChild;
  var lis = ul.children;
  var firstImage = lis[0].firstElementChild;
  var position = 0;
  var height = 190; //height slide + margin

  lis[0].classList.add("active");
  imageFull.src = firstImage.src;
  if (imageZoom) {
    imageZoom.style.backgroundImage = "url('" +firstImage.src +"')";
    imageZone.style.backgroundImage = "url('" +firstImage.src +"')";
  }
  imageFull.setAttribute("data-number-active", 0)

  for (var i = 0; i < lis.length; i++) {
    lis[i].querySelector("img").setAttribute("data-number", i);
  }

  if (lis.length > 3) {
    imageList.appendChild(createArrow("prev"));
    imageList.appendChild(createArrow("next"));

    var prevArrow = gallery.querySelector(".prev");
    var nextArrow = gallery.querySelector(".next");

    prevArrow.hidden = true;
    prevArrow.addEventListener("click", ulScroll);
    nextArrow.addEventListener("click", ulScroll);
  }

  function createArrow(className) {
    var div = document.createElement("div");
    div.classList.add("arrow");
    div.classList.add(className);
    return div;
  }

  function ulScroll() {
    if (this.classList.contains("prev")) {
      position = Math.min(position + height, 0);
      ul.style.marginTop = position + "px";
    }

    if (this.classList.contains("next")) {
      position = Math.max(position - height, -height * (lis.length - 3));
      ul.style.marginTop = position + "px";
    }

    nextArrow.hidden = false;
    prevArrow.hidden = false;

    if (position == -height * (lis.length - 3)) {
      nextArrow.hidden = true;
    }

    if (position == 0) {
      prevArrow.hidden = true;
    }
  }

  function galleryHandler(event) {
    var target = event.target;

    if (target.dataset.number) {
      imageFull.src = target.src;
      imageFull.dataset.numberActive = target.dataset.number;
      if (imageZoom) {
        imageZoom.style.backgroundImage = "url('" +target.src +"')";
        imageZone.style.backgroundImage = "url('" +target.src +"')";
      }
      for (var i = 0; i < lis.length; i++) {
        lis[i].classList.remove("active");
      }

      target.parentNode.classList.add("active");
    }
  }

  function move(event) {
    var imageCoords = imageFull.getBoundingClientRect();
    var imageHeight  = imageFull.offsetHeight;
    var imageWidth = imageFull.offsetWidth;
    var mouseX = event.clientX - imageCoords.left;
    var mouseY = event.clientY - imageCoords.top;
    var zone = {
      left: Math.max(Math.min(mouseX - imageZone.offsetWidth/2, imageWidth - imageZone.offsetWidth), 0),
      top: Math.max(Math.min(mouseY - imageZone.offsetHeight/2, imageHeight - imageZone.offsetHeight), 0)
    };
    var relation =  imageZoom.offsetWidth / imageZone.offsetWidth;



    imageZone.style.backgroundSize = imageFull.offsetWidth + "px";
    imageZone.style.backgroundPositionX = -zone.left + "px";
    imageZone.style.backgroundPositionY = -zone.top + "px";

    imageZone.style.left = zone.left  + "px";
    imageZone.style.top = zone.top  + "px";

    imageZoom.style.backgroundSize = imageWidth * relation + "px";
    imageZoom.style.backgroundPositionX = -zone.left * relation+ "px";
    imageZoom.style.backgroundPositionY = -zone.top * relation+ "px";

  }
  function zoomImageOver(event) {
    if (this.classList.contains("image-full")) {
      imageZoom.style.display = "block";
      imageZone.style.display = "block";
      imageFade.style.visibility = "visible";
      imageFade.style.opacity = "0.5";
      move(event);
    }
  }
  function zoomImageOut(event) {
    if (this.classList.contains("image-full")) {
      imageZoom.style.display = "none";
      imageZone.style.display = "none";
      imageFade.style.visibility = "hidden";
      imageFade.style.opacity = "0";
    }
  }
  function zoomImageMove(event) {
    if (this.classList.contains("image-full")) {
      move(event);
    }
  }

  if (imageZoom) {
    imageFullContainer.addEventListener("mousemove", zoomImageMove);
    imageFullContainer.addEventListener("mouseover", zoomImageOver);
    imageFullContainer.addEventListener("mouseout", zoomImageOut);
  }
  gallery.addEventListener("click", galleryHandler);
  gallery.onmousedown = gallery.onselectstart = function(){return false;}
}

function initShelf() {
  var shelf = document.querySelector(".shelf");
  if (!shelf) return;

  var images = shelf.querySelectorAll("img");
  for (var i = 0; i < images.length; i++) {
    images[i].addEventListener("click", showFullImage);
  }

  function showFullImage(event) {
    var image = event.currentTarget;
    var modal = document.createElement("div");
    var img = document.createElement("img");
    var exit = document.createElement("div");
    img.src = image.src;
    exit.innerHTML = "&#10060;";
    exit.addEventListener("click", closeModal);
    modal.appendChild(img);
    modal.appendChild(exit);
    exit.classList.add("exit");
    modal.classList.add("modal");
    document.body.appendChild(modal);
    document.body.style.overflow = "hidden";
    document.body.style.paddingRight = "18px";

    function closeModal() {
        document.body.removeChild(modal);
        document.body.style.overflow = "";
        document.body.style.paddingRight = "";
    }
  }
}

function initFixedBlocks() {
  var block = document.querySelectorAll(".sticky-block");

  for (var i = 0; i < block.length; i++) {
    moveBlock( block[i]);
  }


  function moveBlock( block, event) {
    var a = document.documentElement.clientHeight;
    var c = document.querySelectorAll(".content")[0].offsetHeight;
    var b = block.offsetHeight+40;
    if (a < b || c <= b) return;
    var container = block.parentNode;
    var containerCoords = container.getBoundingClientRect();
    var blockCoords = block.getBoundingClientRect();
    var blockHeight = block.offsetHeight;

    if(containerCoords.top - 20  < 0  ){
        block.classList.remove("stop")
        block.classList.add("sticky")
    }
    if(containerCoords.top > blockCoords.top){
        block.classList.remove("sticky")
    }
    if(containerCoords.bottom - blockHeight - 40  < 0){
        block.classList.remove("sticky")
            block.classList.add("stop")
    }
  }
}

function initFilterRange() {
  var filters = document.querySelectorAll(".filter-range");

  for (var i = 0; i < filters.length; i++) {
    init(filters[i]);
  }

  function init(filter) {
    var inputMin = filter.querySelector(".inputs input.min");
    var inputMax = filter.querySelector(".inputs input.max");
    var min = Number(inputMin.getAttribute("placeholder"));
    var max = Number(inputMax.getAttribute("placeholder"));

    inputMin.addEventListener("input", validate);
    inputMax.addEventListener("input", validate);
    inputMin.addEventListener("blur", checkValue);
    inputMax.addEventListener("blur", checkValue);

    function validate() {
      this.value = this.value.replace(/[^0-9]/gim,"");
    }
    function checkValue() {
      if (!this.value) return;
      if(this.value > max) this.value = max;
      if(this.value < min) this.value = min;
    }
  }
}

function initFilterAmount() {
  var filters = document.querySelectorAll(".filter-amount");

  for (var i = 0; i < filters.length; i++) {
    init(filters[i]);
  }

  function init(filter) {
    var plus = filter.querySelector(".plus");
    var minus = filter.querySelector(".minus");
    var input = filter.querySelector(".amount input");



    plus.onmousedown = plus.onselectstart = function(){return false;}
    minus.onmousedown = plus.onselectstart = function(){return false;}

    plus.addEventListener("click", Plus);
    minus.addEventListener("click", Minus);
    input.addEventListener("focus", validate);
    input.addEventListener("input", validate);
    input.onkeypress = function(e) {
      e = e || event;


      if (e.keyCode == 8 || e.keyCode == 9) return;
      if (e.keyCode == 37 ||  e.keyCode == 39 ) return;
      if (e.ctrlKey || e.shiftKey) {
        input.dispatchEvent(CEvent);
        return;
      }
      var chr = e.charCode ;

      if (chr == null) return;
      if (chr < 48 || chr > 57) {
        return false;
      }
    }

    function Plus(){
        input.focus();
        var num = + input.value
        num += 1;
        input.value = num;
        input.dispatchEvent(CEvent);
    }

    function Minus(){
        input.focus();
        var  num = + input.value

        if (num > 0){
          num -= 1;
          input.value = num;
          input.dispatchEvent(CEvent);
        }
        if (num == 0){
          input.value = "";

        }
    }

    function validate() {
      input.dispatchEvent(CEvent);
      this.value = this.value.replace(/[^0-9]/gim,"");
      if (this.value == 0) {
        this.value = "";
      }
    }
  }
}

function initColorPalette() {
  var list = document.querySelectorAll("span.color");
  if(list){
    for (var i = 0; i < list.length; i++) {
      var color = list[i].dataset.color.replace(/[^#0-9a-f]/gim,"f");
      if (color[0] == "#") {
        list[i].style.background = color;
      } else {
        list[i].style.background = "#" + color;
      }
    }
  }
}

function initFilterClear() {
  var buttons = document.querySelectorAll(".filter .clear");
  if (buttons) {
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].addEventListener("click", clear)
    }
  }

  function clear(event) {

    var target = event.target;
    var elements = document.querySelectorAll(".open");
    var done = false;

    while (true) {
      if(!target) return;
      if (target.classList.contains("filter")) {
        var inputs = target.querySelectorAll("input");
        for (var i = 0; i < inputs.length; i++) {
          inputs[i].checked = false;
        }
        break;
      }
      target = target.parentNode;
    }
  }
}

var CEvent = new Event("shiftAmountFilter", {bubbles: true});
