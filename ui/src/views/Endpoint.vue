<template>
  <div>
    <b-row class="m-4 p-4">
      <b-card class="bg-light text-dark">
        <b-card-body>
          <b-row>
            <b-col lg='1'></b-col>
            <b-col lg='7' class="d-flex justify-content-lg-start"><h5>{{ endpointHits.endpoint.name }}</h5></b-col>
            <b-col lg='3'><span class='badge text-dark bg-warning'>Expires in {{ endpointHits.endpoint.expires_in }}</span></b-col>
            <b-col lg='1' class="d-flex justify-content-lg-start">
              <b-button pill variant="danger" v-clipboard:copy="endpointHits.endpoint.name" v-clipboard:success="onCopy">Copy</b-button>
            </b-col>
          </b-row>
        </b-card-body>
      </b-card>
    </b-row>
    <b-row v-for="hit in endpointHits.hits" class="m-4 p-4">
      <b-card class="bg-light text-dark">
        <b-row>
            <b-col lg='1'></b-col>
            <b-col class="d-flex justify-content-lg-start"><h4>Query Param</h4></b-col>
            <b-col></b-col>
            <b-col lg='2' class="d-flex justify-content-lg-center">{{ hit.last_hit }}</b-col>
        </b-row>
        <b-row class="mb-4">
          <b-col lg='1'></b-col>
          <b-col class="d-flex justify-content-lg-start">{{ hit.query_param }}</b-col>
          <b-col></b-col>
          <b-col></b-col>
        </b-row>
        <b-row>
          <b-col lg='1'></b-col>
          <b-col class="d-flex justify-content-start"><h4>Raw Body</h4></b-col>
          <b-col></b-col>
          <b-col></b-col>
        </b-row>
        <b-row class="mb-4">
          <b-col lg='1'></b-col>
          <b-col class="d-flex justify-content-start">{{ hit.raw_body }}</b-col>
        </b-row>
        <b-row>
          <b-col lg='1'></b-col>
          <b-col class="d-flex justify-content-start"><h4>Headers</h4></b-col>
          <b-col></b-col>
          <b-col></b-col>
        </b-row>
        <b-row v-for="header in hit.headers">
          <b-col lg='1'></b-col>
          <b-col class="d-flex justify-content-start">{{ header }}</b-col>
          <b-col></b-col>
          <b-col></b-col>
        </b-row>
      </b-card>
    </b-row>
  </div>
</template>
<script>
import Endpoints from '../apis/endpoints/endpoints-api'
import NotFound from '../views/NotFound'
export default {
  name: '',
  data () {
    return {
      endpointHits: null
    }
  },
  created () {
    Endpoints.getEndpointWithHits(this.$route.params.Endpoint).then(response => {
      this.endpointHits = response.data
    }).catch(error => {
      console.log(error)
      this.$router.push('NotFound');
    })
  },
  methods: {
    onCopy(e) {
      // alert('You just copied the following text to the clipboard: ' + e.text)
      this.$bvToast.toast(`${e.text}`, {
          title: 'You just copied the following text to the clipboard',
          autoHideDelay: 5000,
          toaster: 'b-toaster-top-center',
          variant: 'danger',
          solid: true,
          noCloseButton: true,
        })
    }
  }
}
</script>

