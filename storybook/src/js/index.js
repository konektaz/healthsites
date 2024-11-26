const nav = document.querySelector('header[role="banner"] nav')
const closenav = document.querySelector('a#nav-close')
const opennav = document.querySelector('a#menu')

// set focus to our open/close buttons after animation
nav.addEventListener('transitionend', e => {
  if (e.propertyName !== 'transform')
    return

  const isOpen = document.location.hash === '#nav-open'

  isOpen
    ? closenav.focus()
    : opennav.focus()

  if (!isOpen) {
    history.replaceState(history.state, '')
  }
})

opennav.addEventListener('click', e => {
  const isOpen = document.location.hash === '#nav-open'

  if (isOpen) {
    window.history.length
      ? window.history.back()
      : document.location.hash = ''
  }
})

// close our menu when esc is pressed
nav.addEventListener('keyup', e => {
  if (e.code === 'Escape')
    window.history.length
      ? window.history.back()
      : document.location.hash = ''
})