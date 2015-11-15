###*
* Theme: Montran Admin Template
* Author: Coderthemes
* Module/App: Main Js
###

executeFunctionByName = (functionName, context) ->
  args = [].slice.call(arguments).splice(2)
  namespaces = functionName.split('.')
  func = namespaces.pop()
  i = 0
  while i < namespaces.length
    context = context[namespaces[i]]
    i++
  context[func].apply this, args

resizeitems = ->
  if $.isArray(resizefunc)
    i = 0
    while i < resizefunc.length
      window[resizefunc[i]]()
      i++
  return

initscrolls = ->
  if jQuery.browser.mobile != true
    #SLIM SCROLL
    $('.slimscroller').slimscroll
      height: 'auto'
      size: '5px'
    $('.slimscrollleft').slimScroll
      height: 'auto'
      position: 'right'
      size: '5px'
      color: '#7A868F'
      wheelStep: 5
  return

toggle_slimscroll = (item) ->
  if $('#wrapper').hasClass('enlarged')
    $(item).css('overflow', 'inherit').parent().css 'overflow', 'inherit'
    $(item).siblings('.slimScrollBar').css 'visibility', 'hidden'
  else
    $(item).css('overflow', 'hidden').parent().css 'overflow', 'hidden'
    $(item).siblings('.slimScrollBar').css 'visibility', 'visible'
  return

!(($) ->
  'use strict'

  Sidemenu = ->
    @$body = $('body')
    @$openLeftBtn = $('.open-left')
    @$menuItem = $('#sidebar-menu a')
    return

  Sidemenu::openLeftBar = ->
    $('#wrapper').toggleClass 'enlarged'
    $('#wrapper').addClass 'forced'
    if $('#wrapper').hasClass('enlarged') and $('body').hasClass('fixed-left')
      $('body').removeClass('fixed-left').addClass 'fixed-left-void'
    else if !$('#wrapper').hasClass('enlarged') and $('body').hasClass('fixed-left-void')
      $('body').removeClass('fixed-left-void').addClass 'fixed-left'
    if $('#wrapper').hasClass('enlarged')
      $('.left ul').removeAttr 'style'
    else
      $('.subdrop').siblings('ul:first').show()
    toggle_slimscroll '.slimscrollleft'
    $('body').trigger 'resize'
    return

Sidemenu::menuItemClick = (e) ->
    if !$('#wrapper').hasClass('enlarged')
      if $(this).parent().hasClass('has_sub')
        e.preventDefault()
      if !$(this).hasClass('subdrop')
        # hide any open menus and remove all other classes
        $('ul', $(this).parents('ul:first')).slideUp 350
        $('a', $(this).parents('ul:first')).removeClass 'subdrop'
        $('#sidebar-menu .pull-right i').removeClass('md-remove').addClass 'md-add'
        # open our new menu and add the open class
        $(this).next('ul').slideDown 350
        $(this).addClass 'subdrop'
        $('.pull-right i', $(this).parents('.has_sub:last')).removeClass('md-add').addClass 'md-remove'
        $('.pull-right i', $(this).siblings('ul')).removeClass('md-remove').addClass 'md-add'
      else if $(this).hasClass('subdrop')
        $(this).removeClass 'subdrop'
        $(this).next('ul').slideUp 350
        $('.pull-right i', $(this).parent()).removeClass('md-remove').addClass 'md-add'
    return

Sidemenu::init = ->
    $this = this
    #bind on click
    $('.open-left').click (e) ->
      e.stopPropagation()
      $this.openLeftBar()
      return
    # LEFT SIDE MAIN NAVIGATION
    $this.$menuItem.on 'click', $this.menuItemClick
    # NAVIGATION HIGHLIGHT & OPEN PARENT
    $('#sidebar-menu ul li.has_sub a.active').parents('li:last').children('a:first').addClass('active').trigger 'click'
    return

$.Sidemenu = new Sidemenu
$.Sidemenu.Constructor = Sidemenu
)(window.jQuery)
(($) ->
  'use strict'

  FullScreen = ->
    @$body = $('body')
    @$fullscreenBtn = $('#btn-fullscreen')
    return

  #turn on full screen
  # Thanks to http://davidwalsh.name/fullscreen

  FullScreen::launchFullscreen = (element) ->
    if element.requestFullscreen
      element.requestFullscreen()
    else if element.mozRequestFullScreen
      element.mozRequestFullScreen()
    else if element.webkitRequestFullscreen
      element.webkitRequestFullscreen()
    else if element.msRequestFullscreen
      element.msRequestFullscreen()
    return

FullScreen::exitFullscreen = ->
    if document.exitFullscreen
      document.exitFullscreen()
    else if document.mozCancelFullScreen
      document.mozCancelFullScreen()
    else if document.webkitExitFullscreen
      document.webkitExitFullscreen()
    return

FullScreen::toggle_fullscreen = ->
    $this = this
    fullscreenEnabled = document.fullscreenEnabled or document.mozFullScreenEnabled or document.webkitFullscreenEnabled
    if fullscreenEnabled
      if !document.fullscreenElement and !document.mozFullScreenElement and !document.webkitFullscreenElement and !document.msFullscreenElement
        $this.launchFullscreen document.documentElement
      else
        $this.exitFullscreen()
    return

FullScreen::init = ->
    $this = this
    #bind
    $this.$fullscreenBtn.on 'click', ->
      $this.toggle_fullscreen()
      return
    return

$.FullScreen = new FullScreen
$.FullScreen.Constructor = FullScreen
)(window.jQuery)
(($) ->
  'use strict'

  ###*
  Portlet Widget
  ###

  Portlet = ->
    @$body = $('body')
    @$portletIdentifier = '.portlet'
    @$portletCloser = '.portlet a[data-toggle="remove"]'
    @$portletRefresher = '.portlet a[data-toggle="reload"]'
    return

  #on init

  Portlet::init = ->
    # Panel closest
    $this = this
    $(document).on 'click', @$portletCloser, (ev) ->
      ev.preventDefault()
      $portlet = $(this).closest($this.$portletIdentifier)
      $portlet_parent = $portlet.parent()
      $portlet.remove()
      if $portlet_parent.children().length == 0
        $portlet_parent.remove()
      return
    # Panel Reload
    $(document).on 'click', @$portletRefresher, (ev) ->
      ev.preventDefault()
      $portlet = $(this).closest($this.$portletIdentifier)
      # This is just a simulation, nothing is going to be reloaded
      $portlet.append '<div class="panel-disabled"><div class="loader-1"></div></div>'
      $pd = $portlet.find('.panel-disabled')
      setTimeout (->
        $pd.fadeOut 'fast', ->
          $pd.remove()
          return
        return
      ), 500 + 300 * Math.random() * 5
      return
    return

$.Portlet = new Portlet
$.Portlet.Constructor = Portlet
)(window.jQuery)
(($) ->
  'use strict'

  MoltranApp = ->
    @VERSION = '1.0.0'
    @AUTHOR = 'Coderthemes'
    @SUPPORT = 'coderthemes@gmail.com'
    @pageScrollElement = 'html, body'
    @$body = $('body')
    return

  #initializing tooltip

  MoltranApp::initTooltipPlugin = ->
    $.fn.tooltip and $('[data-toggle="tooltip"]').tooltip()
    return

MoltranApp::initPopoverPlugin = ->
    $.fn.popover and $('[data-toggle="popover"]').popover()
    return

MoltranApp::initNiceScrollPlugin = ->
    #You can change the color of scroll bar here
    $.fn.niceScroll and $('.nicescroll').niceScroll(
      cursorcolor: '#9d9ea5'
      cursorborderradius: '0px')
    return

MoltranApp::initKnob = ->
    if $('.knob').length > 0
      $('.knob').knob()
    return

MoltranApp::onDocReady = (e) ->
    FastClick.attach document.body
    resizefunc.push 'initscrolls'
    resizefunc.push 'changeptype'
    $('.animate-number').each ->
      $(this).animateNumbers $(this).attr('data-value'), true, parseInt($(this).attr('data-duration'))
      return
    #RUN RESIZE ITEMS
    $(window).resize debounce(resizeitems, 100)
    $('body').trigger 'resize'
    # right side-bar toggle
    $('.right-bar-toggle').on 'click', (e) ->
      e.preventDefault()
      $('#wrapper').toggleClass 'right-bar-enabled'
      return
    return

MoltranApp::init = ->
    $this = this
    @initTooltipPlugin()
    @initPopoverPlugin()
    @initNiceScrollPlugin()
    @initKnob()
    $(document).ready($this.onDocReady)
    #creating portles
    $.Portlet.init()
    #init side bar - left
    $.Sidemenu.init()
    #init fullscreen
    $.FullScreen.init()
    return

$.MoltranApp = new MoltranApp
$.MoltranApp.Constructor = MoltranApp
)(window.jQuery)
(($) ->
  'use strict'
  $.MoltranApp.init()
  return
)(window.jQuery)

### ------------ some utility functions ----------------------- ###

#this full screen

toggle_fullscreen = ->

w = undefined
h = undefined
dw = undefined
dh = undefined

changeptype = ->
  w = $(window).width()
  h = $(window).height()
  dw = $(document).width()
  dh = $(document).height()
  if jQuery.browser.mobile == true
    $('body').addClass('mobile').removeClass 'fixed-left'
  if !$('#wrapper').hasClass('forced')
    if w > 990
      $('body').removeClass('smallscreen').addClass 'widescreen'
      $('#wrapper').removeClass 'enlarged'
    else
      $('body').removeClass('widescreen').addClass 'smallscreen'
      $('#wrapper').addClass 'enlarged'
      $('.left ul').removeAttr 'style'
    if $('#wrapper').hasClass('enlarged') and $('body').hasClass('fixed-left')
      $('body').removeClass('fixed-left').addClass 'fixed-left-void'
    else if !$('#wrapper').hasClass('enlarged') and $('body').hasClass('fixed-left-void')
      $('body').removeClass('fixed-left-void').addClass 'fixed-left'
  toggle_slimscroll '.slimscrollleft'
  return

debounce = (func, wait, immediate) ->
  timeout = undefined
  result = undefined
  ->
    context = this
    args = arguments

    later = ->
      timeout = null
      if !immediate
        result = func.apply(context, args)
      return

    callNow = immediate and !timeout
    clearTimeout timeout
    timeout = setTimeout(later, wait)
    if callNow
      result = func.apply(context, args)
    result

wow = new WOW(
  boxClass: 'wow'
  animateClass: 'animated'
  offset: 50
  mobile: false)
wow.init()