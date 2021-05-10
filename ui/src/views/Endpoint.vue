<template>
  <div>
    <div>
      <span>{{ endpointHits.endpoint.name }}     </span><span>     Expires in {{ endpointHits.endpoint.expires_in }}</span><span><button>Copy</button></span>
    </div>
    <div v-for="hit in endpointHits.hits">
      <div>
        <div><h4><span>Query Param</span><span>     {{ hit.last_hit }}</span></h4></div>
        <div>{{ hit.query_param }}</div>
        <div>
          <div><h4>Raw Body</h4></div>
          <div>{{ hit.raw_body }}</div>
        </div>
        <div>
          <div><h4>Headers</h4></div>
          <div v-for="header in hit.headers">
            <div>{{ header }}</div>
          </div>
        </div>
        <!-- <div>{{ hit }}</div> -->
      </div>
    </div>
  </div>
</template>
<script>
import Endpoints from '../apis/endpoints/endpoints-api'
export default {
  name: '',
  data () {
    return {
      endpointHits: null
    }
  },
  created () {
    console.log(this.$route.params.Endpoint)
    Endpoints.getEndpointWithHits(this.$route.params.Endpoint).then(response => {
      this.endpointHits = response.data
    })
  }
}
</script>

