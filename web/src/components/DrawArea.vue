<template>
    <div id="drawarea_wrap">
        <v-card
            id="drawarea"
            max-width="300"
            height="310px"
            flat
        >
            <div id="canvas-area">
                <canvas
                    id="myCanvas"
                    width="300px"
                    height="300px"
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
                <!-- <i class='bx bx-bulb'></i> -->
                <i class='bx bx-question-mark'></i>
                </v-btn>
            </div>
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
            this.context.lineWidth = 5
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
                this.context.lineWidth = 5
                this.context.strokeStyle = '#000000'
            },
            erase: function () {
                this.canvasMode = 'eraser'
                this.context.lineCap = 'square'
                this.context.lineJoin = 'square'
                this.context.lineWidth = 30
                this.context.strokeStyle = '#FFFFFF'
            },
            predict: function () {
                let image = this.canvas.toDataURL('image/png')
                let prev = "data:image/png;base64,"
                image = image.replace(prev, '')
                this.$axios({
                    url: '/api/predict/getPredict/',
                    method: 'POST',
                    data: JSON.stringify({data: image}),
                })
                .then(res => {
                    console.log(res.data)
                })
                .catch(e => {
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
            }
        },
        mixins: [],
    }
</script>
<style lang="scss" scoped>
    #drawarea_wrap {
        #drawarea {
            margin: 0 auto;
            #myCanvas {
                // border: 1px solid black;
                border-radius: 5px;
                box-shadow: 1px 1px 1px rgba(100, 100, 100, 0.5);
            }
        }

        .eraser {
            cursor: url(../assets/img/eraser.png) 15 15 auto;
        }
    }
</style>
