const { Nuxt, Builder } = require('nuxt')
// eslint-disable-next-line no-unused-vars
const request = require('supertest')
const nuxtConfig = require('../nuxt.config.js')

// We keep the nuxt and server instance
// So we can close them at the end of the test
let nuxt = null

// Init Nuxt.js and create a server listening on localhost:4000
beforeAll(async () => {
    // const config = {
    //   dev: process.env.NODE_ENV === 'production',
    //   rootDir: resolve(__dirname, '../'),
    //   mode: 'universal',
    //   plugins,
    //   modules
    // }
  
    nuxt = new Nuxt({...nuxtConfig, server: { port: 3001}, buildDir: '.nuxt-build-jest'})
  
    await new Builder(nuxt).build()
  
    await nuxt.server.listen(3001, 'localhost')
  }, 300000)
  
  // Example of testing only generated html
  describe('GET /', () => {
    test('Route / Renders map-container', async () => {
      const { html } = await nuxt.server.renderRoute('/', {})
  
      expect(html).toContain('map-container')
    })
  })

    // Example of testing only generated html
    describe('GET /login', () => {
        test('Route /login renders', async () => {
          const { html } = await nuxt.server.renderRoute('/login', {})
      
          expect(html).toContain('Login')
        })
      })
  
  // describe('GET /', () => {
  //   test('returns status code 200', async () => {
  //     const response = await request(nuxt.server.app).get('/')
  //     expect(response.statusCode).toBe(200)
  //   })
  // })
  
  // describe('GET /test', () => {
  //   test('returns status code 404', async () => {
  //     const response = await request(nuxt.server.app).get('/test')
  //     expect(response.statusCode).toBe(404)
  //   })
  // })
  
  // Close server and ask nuxt to stop listening to file changes
  afterAll(() => {
    nuxt.close()
  })