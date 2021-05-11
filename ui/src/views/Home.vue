<template>
  <div>

    <h2> Create new HTTP endpoints to inspect the data in user friendly way!</h2>

    <div>
      <b-button pill variant="danger" @click="createNewEndpoint">+ Create New</b-button>
    </div>

    <div>
      <ul>
        <div v-for="item in items">
          <div>{{item.name}} ({{item.clicks}})</div>
          <div>Expires in {{item.expires_in}}</div>
        </div>
      </ul>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import Endpoints from '../apis/endpoints/endpoints-api'

export default {
  name: 'Home',
  data () {
    return {
      createOutputMessage: '',
      items: null,
    }
  },
  components: {
    // HelloWorld
  },
  created () {
    Endpoints.getEndpointsList().then(response => {
      this.items = response.data
    })
  },
  methods: {
    createNewEndpoint () {
      Endpoints.createEndpoint().then(response => {
        this.createOutputMessage = response.data
        Endpoints.getEndpointsList().then(response => {
          this.items = response.data
        })
      })
    }
  }
}
</script>
