<template>
    <div>
        <v-card id="drawarea_wrap">
            <vs-navbar
                v-model="activeitem"
            >
                <div slot="title">
                    <vs-navbar-title>
                        tegakinum
                    </vs-navbar-title>
                </div>

                <vs-navbar-item index="0">
                    <a href="#">Home</a>
                </vs-navbar-item>
                <!-- <vs-navbar-item index="1">
                    <a href="#">Sample</a>
                </vs-navbar-item> -->
            </vs-navbar>

            <v-container>
                <v-row>
                    <v-col cols="6">
                        <v-card
                            id="drawarea"
                            flat
                        >
                            <div id="canvas-area">
                                <canvas
                                    id="myCanvas"
                                    width="400px"
                                    height="400px"
                                    @mousedown="dragStart"
                                    @mouseup="dragEnd"
                                    @mouseout="dragEnd"
                                    @mousemove="draw"
                                    :class="{eraser: canvasMode === 'eraser'}"
                                ></canvas>
                            </div>
                            <div id="tool-area">
                                <v-btn
                                    id="pen-button"
                                    icon
                                    @click="pen"
                                ><i class='bx bx-pencil'></i></v-btn>
                                <v-btn
                                    id="eraser-button"
                                    icon
                                    @click="erase"
                                ><i class='bx bxs-eraser' ></i></v-btn>
                                <v-btn
                                    id="clear-button"
                                    icon
                                    @click="clear"
                                ><i class='bx bx-x'></i></v-btn>
                                <v-btn
                                    id="predict-button"
                                    icon
                                    @click="predict"
                                >
                                <i class='bx bx-bulb'></i>
                                </v-btn>
                            </div>
                        </v-card>
                    </v-col>
                    <v-col cols="6" class="graph">
                        <VueApexCharts
                            class="donut"
                            width="260"
                            height="260"
                            type="donut"
                            :options="chartOptions"
                            :series="pSeries"
                        />
                        <VueApexCharts
                            class="bar"
                            width="300"
                            height="240"
                            type="bar"
                            :options="barChartOptions"
                            :series="series"
                        />
                    </v-col>
                </v-row>
            </v-container>
        </v-card>
    </div>
</template>
<script>
    export default {
        name: 'DrawArea',
        components: {
        },
        props: {
        },
        data: () => ({
            canvasMode: 'pen',
            canvas: null,
            context: null,
            isDrag: false,
            activeitem: 0,
            activeLoading: false,
            series: [
                {
                    data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                }
            ],
            pSeries: [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
            barChartOptions: {
                chart: {
                    type: 'bar',
                },
                plotOptions: {
                    bar: {
                        borderRadius: 4,
                        horizontal: true
                    }
                },
                dataLabels: {
                    enabled: true
                },
                xaxis: {
                    categories: [
                        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    ]
                }
            },
            chartOptions: {
                chart: {
                    type: 'donut',
                },
                labels: [
                    0, 1, 2, 3, 4, 5, 6, 7, 8, 9
                ],
                legend: {
                    show: false,
                },
                dataLabels: {
                    enabled: true
                },
                // theme: {
                //     monochrome: {
                //         enabled: true
                //     }
                // },
                responsive: [{
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 200
                        },
                        legend: {
                            position: 'bottom'
                        }
                    }
                }]
            },
        }),
        beforeCreate () {
        },
        created () {
        },
        beforeMount () {
        },
        mounted () {
            this.canvas = document.querySelector('#myCanvas')
            this.context = this.canvas.getContext('2d')
            this.context.lineCap = 'round'
            this.context.lineJoin = 'round'
            this.context.lineWidth = 25
            this.context.strokeStyle = '#000000'
        },
        beforeUpdate () {
        },
        update () {
        },
        beforeDestroy () {
        },
        destoryd () {
        },
        watch: {
        },
        computed: {
        },
        methods: {
            draw: function (e) {
                const x = e.layerX
                const y = e.layerY

                if (!this.isDrag) {
                    return
                }

                this.context.lineTo(x, y)
                this.context.stroke()
            },
            dragStart: function (e) {
                const x = e.layerX
                const y = e.layerY

                this.context.beginPath()
                this.context.lineTo(x, y)
                this.context.stroke()

                this.isDrag = true
            },
            dragEnd: function () {
                this.context.closePath()
                this.isDrag = false
            },
            pen: function () {
                this.canvasMode = 'pen'
                this.context.lineCap = 'round'
                this.context.lineJoin = 'round'
                this.context.lineWidth = 25
                this.context.strokeStyle = '#000000'
            },
            erase: function () {
                this.canvasMode = 'eraser'
                this.context.lineCap = 'square'
                this.context.lineJoin = 'square'
                this.context.lineWidth = 35
                this.context.strokeStyle = '#FFFFFF'
            },
            predict: function () {
                this.activeLoading = true
                this.$vs.loading({
                    type: 'radius'
                })
                let image = this.canvas.toDataURL('image/png')
                let prev = "data:image/png;base64,"
                image = image.replace(prev, '')
                this.$axios({
                    url: '/api/predict/getPredict/',
                    method: 'POST',
                    data: JSON.stringify({data: image}),
                })
                .then(res => {
                    this.activeLoading = false
                    this.$vs.loading.close()
                    console.log(res.data.result)
                    this.setSeries(res.data.result)
                })
                .catch(e => {
                    this.activeLoading = false
                    this.$vs.loading.close()
                    console.log(e)
                })
            },
            clear: function () {
                this.context.clearRect(
                    0,
                    0,
                    this.context.canvas.clientWidth,
                    this.context.canvas.clientHeight
                )
            },
            setSeries: function (data) {
                this.series = [
                    {
                        data: data
                    }
                ],
                this.pSeries = data.map(Number)
            }
        },
        mixins: [],
    }
</script>
<style lang="scss" scoped>
    #drawarea_wrap {
        width: 900px;
        height: 580px;
        margin: 0 auto;
        #drawarea {
            margin: 40px 0 0 20px;
            #myCanvas {
                border-radius: 5px;
                box-shadow: 1px 1px 1px rgba(100, 100, 100, 0.5);
            }
        }

        .eraser {
            cursor: url(../assets/img/eraser.png) 15 15 auto;
        }

        .graph {
            padding-left: 50px;
            .donut {
                margin-left: 25px;
            }
            .bar {
            }
        }
    }
</style>
