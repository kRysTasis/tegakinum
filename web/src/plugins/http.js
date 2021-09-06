import Vue from 'vue'
import axios from 'axios'

export default {
    install: function (Vue, options) {
        const http = axios.create({
            baseURL: process.env.NODE_ENV !== 'production' ? 'http://localhost:8000/' : `${process.env.VUE_APP_URI}/`,
			xsrfCookieName: 'csrftoken',
			xsrfHeaderName: 'X-CSRFTOKEN',
			timeout: 10000,
        })
        Vue.prototype.$axios = http
    }
}
