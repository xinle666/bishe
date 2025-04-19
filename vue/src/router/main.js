import VueRouter from 'vue-router';
const routes =[
    {
        path:'/',
        name:'login',
        component:()=>import('../components/Login.vue')
    },
    {
        path:'/index',
        name:'index',
        component:()=>import('../components/IndexPage.vue'),
        children:[
            {
                path:'/home',
                name:'home',
                component:()=>import('../components/Home.vue')
            },
            {
                path:'/userControl',
                name:'userControl',
                component:()=>import('../components/userControl.vue')
            },
                  {
                path:'/files',
                name:'files',
                component:()=>import('../components/files.vue')
            },
                   {
                path:'/excel',
                name:'excel',
                component:()=>import('../components/excel.vue')
            },
                {
                path:'/word',
                name:'word',
                component:()=>import('../components/word.vue')
            },
                 {
                path:'/pdf',
                name:'pdf',
                component:()=>import('../components/pdf.vue')
            },
  {
                path:'/projectsControl',
                name:'projectsControl',
                component:()=>import('../components/projectsControl.vue')
            },
              {
                path:'/project',
                name:'project',
                component:()=>import('../components/project.vue')
            },
            {
                path:'/userHome',
                name:'userHome',
                component:()=>import('../components/UserHome.vue')
            },

        ]
    }

]
const router = new VueRouter({
    mode:'history',
    routes
})
// 全局前置守卫
// router.beforeEach((to, from, next) => {
//     const user = store.state.user; // 假设用户信息保存在 Vuex 的 store 中
//     const isAuthenticated = !!user; // 判断用户是否已登录
//
//     if (to.meta.requiresAuth && !isAuthenticated) {
//         // 如果需要认证且用户未登录，重定向到登录页面
//         next('/');
//     } else if (to.meta.roles && !to.meta.roles.includes(user.role_id)) {
//         // 如果角色不符合要求，重定向到未授权页面或其他页面
//         next('/'); // 或者 `next({ path: '/unauthorized' })`
//     } else {
//         // 允许访问
//         next();
//     }
// });
export default router