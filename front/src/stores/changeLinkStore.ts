import { defineStore } from 'pinia';
import axios from 'axios';

interface ChangeLinkStore {
    status: number;
    message: string;
    in_progress: boolean;
}

export const useChangeLinkStore = defineStore('changeLink', {
    state: (): ChangeLinkStore => ({
    status: 502,
    message: "Bad Gateway",
    in_progress: false,
    }),
    actions: {
        async changeLink(shared_link: string, tg_id: string) {
            try {
                this.in_progress = true
                const response = await axios.post(
                'WEBAPP_FRONT_LINK/change_link',
                {
                    shared_link: shared_link,
                    tg_id: tg_id.toString()
                });
                if (response.status === 200) {
                    this.status = response.data.status;
                    this.message = response.data.message;
                    this.in_progress = false;
                }
            } catch (error) {
                this.message = 'error at response:' + error
                this.in_progress = false;
            } finally {
                this.in_progress = false;
            }
        },
    },
});
