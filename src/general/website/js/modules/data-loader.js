import { CONFIG } from '../general/config.js';

export class DataLoader {
    constructor() {
        this.cache = new Map();
    }

    async loadJSON(path) {
        if (this.cache.has(path)) {
            return this.cache.get(path);
        }

        try {
            const response = await fetch(`${CONFIG.API_BASE}${path}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();
            this.cache.set(path, data);
            return data;
        } catch (error) {
            console.error('Error loading data:', error);
            throw error;
        }
    }

    async loadMember(memberId) {
        return this.loadJSON(`${CONFIG.MEMBERS_PATH}member${memberId}.json`);
    }

    async loadAllMembers(memberIds) {
        const promises = memberIds.map(id => this.loadMember(id));
        return Promise.all(promises);
    }

    async loadPublications() {
        return this.loadJSON(`${CONFIG.PUBLICATIONS_PATH}publications.json`);
    }
}