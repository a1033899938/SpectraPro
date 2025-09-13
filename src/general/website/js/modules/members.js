import { DataLoader } from '../data-loader.js';
import { UIComponents } from '../ui-components.js';
import { SELECTORS } from '../config.js';

export class MembersModule {
    constructor(dataLoader) {
        this.dataLoader = dataLoader;
        this.members = [];
    }

    async init() {
        await this.loadMembers();
        this.renderMembers();
    }

    async loadMembers() {
        const memberIds = [1, 2, 3, 4, 5]; // 从配置获取或动态生成
        this.members = await this.dataLoader.loadAllMembers(memberIds);
    }

    renderMembers() {
        const container = document.querySelector(SELECTORS.MEMBERS_CONTAINER);
        if (container) {
            UIComponents.renderList(container, this.members, UIComponents.createMemberCard);
        }
    }

    filterMembers(searchTerm) {
        const filtered = this.members.filter(member =>
            member.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            member.research.toLowerCase().includes(searchTerm.toLowerCase())
        );

        const container = document.querySelector(SELECTORS.MEMBERS_CONTAINER);
        UIComponents.renderList(container, filtered, UIComponents.createMemberCard);
    }
}