const { Nuxt, Builder } = require('nuxt')
// eslint-disable-next-line no-unused-vars
const request = require('supertest')
const nuxtConfig = require('../nuxt.config.js')

// We keep the nuxt and server instance
// So we can close them at the end of the test
let nuxt = null

// Init Nuxt.js and create a server listening on localhost:4000
beforeAll(async () => {
  nuxt = new Nuxt({ ...nuxtConfig, server: { port: 3001 }, buildDir: '.nuxt-build-jest' })

  await new Builder(nuxt).build()

  await nuxt.server.listen(3001, 'localhost')
}, 300000)

// Test if / renders
describe('index test', () => {
  test('Route / Renders map-container', async () => {

    const { html } = await nuxt.server.renderRoute('/', {})
    expect(html).toContain('map-container')

  })
})

// Test if /login renders
describe('GET /login', () => {
  test('Route /login renders', async () => {
    const { html } = await nuxt.server.renderRoute('/login', {})

    expect(html).toContain('Login')
  })
})

// Test if /booking renders
describe('GET /booking', () => {
  test('Route /booking renders', async () => {
    const { html } = await nuxt.server.renderRoute('/booking', {})

    expect(html).toContain('Booking');
    expect(html).toContain('Please select your date and time');
  })
})

// Test if /list renders
describe('GET /list', () => {
  test('Route /list renders', async () => {
    const { html } = await nuxt.server.renderRoute('/list', {})

    expect(html).toContain('Buy as soon as possible');
  })
})

// Test if /qrcode renders
describe('GET /qrcode', () => {
  test('Route /qrcode renders', async () => {
    const { html } = await nuxt.server.renderRoute('/qrcode', {})

    expect(html).toContain('qr-code-container');
  })
})

// Test if /register renders
describe('GET /register', () => {
  test('Route /register renders', async () => {
    const { html } = await nuxt.server.renderRoute('/register', {})

    expect(html).toContain('register-container');
  })
})


// Close server and ask nuxt to stop listening to file changes
afterAll(() => {
  nuxt.close()
})