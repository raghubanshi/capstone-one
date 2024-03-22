document.addEventListener('DOMContentLoaded', () => {
    const savedNewsList = document.getElementById('saved-news-list');

    // Add event listener to handle unsave button clicks
    savedNewsList.addEventListener('click', (event) => {
        if (event.target.classList.contains('unsave-btn')) {
            const newsId = event.target.dataset.newsId;
            unsaveNews(newsId); // Call function to unsave news
        }
    });

    function unsaveNews(newsId) {
        // Send data to Flask backend to unsave news
        axios.post('/unsave-news', { news_id: newsId })
            .then(response => {
                alert('News unsaved successfully!');
                // Remove the saved news article from the frontend
                const articleElement = document.querySelector(`[data-news-id="${newsId}"]`);
                if (articleElement) {
                    articleElement.parentElement.parentElement.parentElement.remove(); // Remove the <li> element
                }
            })
            .catch(error => {
                console.error('Error unsaving news:', error);
                alert('Error unsaving news. Please try again.');
            });
    }
});