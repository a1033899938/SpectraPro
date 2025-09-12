export class UIComponents {
    static createMemberCard(member) {
        return `
            <div class="member-card" data-member-id="${member.id}">
                <div class="member-image">
                    <img src="${member.image}" alt="${member.name}" 
                         onerror="this.src='Images/default-avatar.jpg'">
                </div>
                <div class="member-info">
                    <h3>${member.name}</h3>
                    <p class="member-title">${member.title}</p>
                    <p class="member-research">${member.research}</p>
                    <a href="mailto:${member.email}" class="member-email">${member.email}</a>
                </div>
            </div>
        `;
    }

    static createPublicationItem(publication) {
        return `
            <div class="publication-item" data-pub-id="${publication.id}">
                <div class="pub-title">${publication.title}</div>
                <div class="pub-authors">${publication.authors}</div>
                <div class="pub-details">
                    ${publication.journal ? `<em>${publication.journal}</em>` : ''}
                    ${publication.volume ? `, ${publication.volume}` : ''}
                    ${publication.pages ? `: ${publication.pages}` : ''}
                </div>
            </div>
        `;
    }

    static renderList(container, items, createItemFn) {
        container.innerHTML = items.map(item => createItemFn(item)).join('');
    }
}