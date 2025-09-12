import { DataLoader } from './data-loader.js';
import { UIComponents } from './ui-components.js';
import { SELECTORS } from './config.js';

export class EventHandlers {
    constructor(dataLoader) {
        this.dataLoader = dataLoader;
        this.initEvents();
    }

    initEvents() {
        this.handleMemberClick();
        this.handlePublicationFilter();
        this.handleSearch();
    }

    handleMemberClick() {
        document.addEventListener('click', (e) => {
            const memberCard = e.target.closest('.member-card');
            if (memberCard) {
                const memberId = memberCard.dataset.memberId;
                this.showMemberDetail(memberId);
            }
        });
    }

    async showMemberDetail(memberId) {
        try {
            const member = await this.dataLoader.loadMember(memberId);
            this.showModal('member-detail', member);
        } catch (error) {
            console.error('Error loading member details:', error);
        }
    }

    handleSearch() {
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.addEventListener('input', this.debounce((e) => {
                this.filterContent(e.target.value);
            }, 300));
        }
    }

    debounce(func, delay) {
        let timeoutId;
        return (...args) => {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }
}