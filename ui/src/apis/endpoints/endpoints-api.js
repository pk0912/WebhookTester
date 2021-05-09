import http from '../../utils/http-common'

export default class Endpoints {
    static getEndpointsList () {
        return http.get("index/")
    }

    static createEndpoint () {
        return http.post("index/")
    }

    static getEndpointWithHits (parameter) {
        return http.get("/"+parameter+"/")
    }


}