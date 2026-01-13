import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import App from '../App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createTestingPinia } from '@pinia/testing'

const routes = [
  { path: '/', component: { template: '<div></div>' }, meta: { hideHeader: false } },
  { path: '/create', component: { template: '<div></div>' }, meta: { hideHeader: false } },
  { path: '/join', component: { template: '<div></div>' }, meta: { hideHeader: false } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

describe('App', () => {
  it('renders properly', async () => {
    router.push('/')
    await router.isReady()
    const wrapper = mount(App, {
      global: {
        plugins: [router, createTestingPinia({
          createSpy: vi.fn,
        })]
      }
    })
    expect(wrapper.text()).toContain('AuraVibe')
  })
})
