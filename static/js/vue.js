const compoapp = Vue.createApp({})

compoapp.component('component-a', {
  methods: {
      foo: function(e) {
                alert("compo-a")
            }
  }
})
compoapp.component('component-b', {
  /* ... */
})
compoapp.component('component-c', {
  /* ... */
})

compoapp.mount('#compoapp')