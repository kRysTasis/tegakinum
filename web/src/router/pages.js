import { Home, NotFound } from '@/views/index'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home,
        meta: {
            description: 'ホーム'
        }
    },
    {
        path: '*',
        name: 'NotFound',
        component: NotFound
    }
]

export default routes
