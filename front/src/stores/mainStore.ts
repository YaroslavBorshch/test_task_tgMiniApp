import { defineStore } from 'pinia';
import axios from 'axios';
import {ref} from "vue";

interface MainStore {
    status: number;
    message: string;
    tg_info: object;
    user_exist: boolean;
    test: any;
    from_login: boolean;
}

export const useMainStore = defineStore('user', {
    state: (): MainStore => ({
    status: 502,
    message: "Bad Gateway",
    tg_info: {},
    user_exist: false,
    test: '',
    from_login: false,
    }),
    actions: {
        // Отправляемся на эндпоинт входа+сохранения пользователя
        async login(birthday: string, tg_info: string) {
            try {
                const response = await axios.post(
                'WEBAPP_BACK_LINK/login',
                {
                    birthday: birthday,
                    tg_info: tg_info
                });
                if (response.data) {
                    this.message = response.data.message;
                    this.status = response.data.status;
                    this.user_exist = response.data.user_exist;
                    this.tg_info = response.data.user_info;
                    this.test = response.data;
                    this.from_login = true;
                }
            } catch (error) {
                this.message = 'error at response:' + error;
            } finally {
                this.message = 'wtf';
            }
        },


        async fetchUserData(shared_link: string, tg_info: string) {
            try {
                const response = await axios.post(
                'WEBAPP_BACK_LINK/load_user_info',
                {
                    shared_link: shared_link,
                    tg_info: tg_info
                });
                if (response.data) {
                    this.message = response.data.message;
                    this.status = response.data.status;
                    this.user_exist = response.data.user_exist;
                    this.tg_info = response.data.user_info;
                    this.test = response.data;
                }
            } catch (error) {
                this.message = 'error at response:' + error;
            }
        },
    },
});
