// 导入模块
import { CONFIG, SELECTORS } from './config.js';
import { DataLoader } from './data-loader.js';
import { EventHandlers } from './events.js';
import { MembersModule } from './modules/members.js';
import { PublicationsModule } from './modules/publications.js';
import { CarouselModule } from './modules/carousel.js';

// 初始化应用
class App {
    constructor() {
        this.dataLoader = new DataLoader();
        this.eventHandlers = new EventHandlers(this.dataLoader);
        this.initModules();
    }

    async initModules() {
        // 初始化各功能模块
        this.membersModule = new MembersModule(this.dataLoader);
        this.publicationsModule = new PublicationsModule(this.dataLoader);
        this.carouselModule = new CarouselModule();

        // 加载数据
        await Promise.all([
            this.membersModule.init(),
            this.publicationsModule.init(),
            this.carouselModule.init()
        ]);
    }
}

// 启动应用
document.addEventListener('DOMContentLoaded', () => {
    new App();
});

// 导出供其他模块使用
export { App };