document.addEventListener('DOMContentLoaded', () => {
    const newsList = document.getElementById('news-list');
    const filterForm = document.getElementById('filter-form');
    const filterBtn = document.getElementById('filter-btn');
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');

    // Fetch news articles initially when the page loads
    fetchNews();

    filterBtn.addEventListener('click', (e) => {
        e.preventDefault();
        fetchNews();
    });

    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const searchTerm = searchInput.value.trim();
        if (searchTerm) {
            fetchNews(searchTerm);
        }
    });

    function fetchNews(searchTerm = '') {
        const category = document.getElementById('category').value;
        const country = document.getElementById('country').value;

        if (searchTerm.length > 2) {
            axios.get('/news', {
                params: { q: searchTerm}
            })
                .then(response => {
                    const articles = response.data.articles;

                    // Clear previous news articles
                    newsList.innerHTML = '';

                    articles.forEach(article => {
                        const colDiv = document.createElement('div');
                        colDiv.classList.add('col-md-4', 'mb-4');
    
                        const cardDiv = document.createElement('div');
                        cardDiv.classList.add('card');
    
                        const img = document.createElement('img');
                        img.src = article.urlToImage ? article.urlToImage : 'https://s3-cdn.cmlabs.co/page/2023/01/24/a-guideline-on-how-to-fix-error-404-not-found-effectively-519451.png';
                        img.classList.add('card-img-top');
                        img.alt = article.title;
    
                        const cardBodyDiv = document.createElement('div');
                        cardBodyDiv.classList.add('card-body');
    
                        const aTitle = document.createElement('a');
                        aTitle.href = article.url;
                        aTitle.target = '_blank';
                        aTitle.textContent = article.title;
                        aTitle.classList.add('card-title');

                        const pDescription = document.createElement('p');
                        pDescription.textContent = article.description || 'No description available.';
                        pDescription.classList.add('card-text');
    
                        const saveBtn = document.createElement('button');
                        saveBtn.textContent = 'Save News';
                        saveBtn.classList.add('btn', 'btn-primary');
                        saveBtn.addEventListener('click', () => {
                            saveNews(article.author, article.title, article.description, article.url, article.urlToImage, article.publishedAt, saveBtn); // Call function to save news
                        });
    
                        cardBodyDiv.appendChild(aTitle);
                        cardBodyDiv.appendChild(pDescription);
                        cardBodyDiv.appendChild(saveBtn);
    
                        cardDiv.appendChild(img);
                        cardDiv.appendChild(cardBodyDiv);
    
                        colDiv.appendChild(cardDiv);
    
                        newsList.appendChild(colDiv);
                    });
                    
                })
                .catch(error => {
                    console.error('Error fetching news:', error);
                    alert('Error fetching news. Please try again.');
                });
        }
        else {
            axios.get('/news', {
                params: { q: searchTerm, category: category || '', country: country || 'us' }
            })
                .then(response => {
                    const articles = response.data.articles;

                    // Clear previous news articles
                    newsList.innerHTML = '';

                    articles.forEach(article => {
                        const colDiv = document.createElement('div');
                        colDiv.classList.add('col-md-4', 'mb-4');
    
                        const cardDiv = document.createElement('div');
                        cardDiv.classList.add('card');
    
                        const img = document.createElement('img');
                        img.src = article.urlToImage ? article.urlToImage : 'https://s3-cdn.cmlabs.co/page/2023/01/24/a-guideline-on-how-to-fix-error-404-not-found-effectively-519451.png';
                        img.classList.add('card-img-top');
                        img.alt = article.title;
    
                        const cardBodyDiv = document.createElement('div');
                        cardBodyDiv.classList.add('card-body');
    
                        const aTitle = document.createElement('a');
                        aTitle.href = article.url;
                        aTitle.target = '_blank';
                        aTitle.textContent = article.title;
                        aTitle.classList.add('card-title');

                        const pDescription = document.createElement('p');
                        pDescription.textContent = article.description || 'No description available.';
                        pDescription.classList.add('card-text');
    
                        const saveBtn = document.createElement('button');
                        saveBtn.textContent = 'Save News';
                        saveBtn.classList.add('btn', 'btn-primary');
                        saveBtn.addEventListener('click', () => {
                            saveNews(article.author, article.title, article.description, article.url, article.urlToImage, article.publishedAt, saveBtn); // Call function to save news
                        });
    
                        cardBodyDiv.appendChild(aTitle);
                        cardBodyDiv.appendChild(pDescription);
                        cardBodyDiv.appendChild(saveBtn);
    
                        cardDiv.appendChild(img);
                        cardDiv.appendChild(cardBodyDiv);
    
                        colDiv.appendChild(cardDiv);
    
                        newsList.appendChild(colDiv);
                    });
                    
                })
                .catch(error => {
                    console.error('Error fetching news:', error);
                    alert('Error fetching news. Please try again.');
                });
        }


    }

    function saveNews(author, title, description, url, urlToImage, publishedAt, buttonElement) {
        // Send data to Flask backend to save news
        axios.post('/save-news', {
            author: author,
            title: title,
            description: description,
            url: url,
            url_to_image: urlToImage,
            published_at: publishedAt
        })
            .then(response => {
                alert('News saved successfully!');
                // Hide the button after successful save
                buttonElement.style.display = 'none';
            })
            .catch(error => {
                console.error('Error saving news:', error);
                alert('Error saving news. Please try again.');
            });
    }

});
