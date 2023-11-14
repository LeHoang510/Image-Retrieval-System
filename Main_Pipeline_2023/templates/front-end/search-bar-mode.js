
document.addEventListener('DOMContentLoaded', function () {
    const searchMode = document.getElementById('searchMode');
    const textSearch = document.getElementById('textSearch');
    const sequenceSearch = document.getElementById('sequenceSearch');
    const sequenceSearch2 = document.getElementById('sequenceSearch2');
    const bertSearch = document.getElementById('bertSearch');
    const imgSearch = document.getElementById('imgSearch');
    const searchButton = document.getElementById('searchButton');

    searchMode.addEventListener('change', function () {
        if (searchMode.value === 'Text') {
            textSearch.style.display = 'flex';
            sequenceSearch.style.display = 'none';
            sequenceSearch2.style.display = 'none';
            bertSearch.style.display = 'none';
            imgSearch.style.display = 'none';
        } else if (searchMode.value === 'Sequence') {
            textSearch.style.display = 'none';
            sequenceSearch.style.display = 'block';
            sequenceSearch2.style.display = 'block';
            bertSearch.style.display = 'none';
            imgSearch.style.display = 'none';
        } else if (searchMode.value === 'Bert') {
            textSearch.style.display = 'none';
            sequenceSearch.style.display = 'none';
            sequenceSearch2.style.display = 'none';
            bertSearch.style.display = 'block';
            imgSearch.style.display = 'none';
        } else if (searchMode.value === 'Image') {
            textSearch.style.display = 'none';
            sequenceSearch.style.display = 'none';
            sequenceSearch2.style.display = 'none';
            bertSearch.style.display = 'none';
            imgSearch.style.display = 'block';
        }
    });

    searchButton.addEventListener('click', function () {
        if (searchMode.value === 'Text') {
            const textQuery = document.getElementById('textQuery').value;
            window.location.href = "/textsearch?textquery=" + textQuery;
        } else if (searchMode.value === 'Sequence') {
            const sequence1 = document.getElementById('sequence1').value;
            const sequence2 = document.getElementById('sequence2').value;
            window.open("/sequencesearch?text_start=" + sequence1 + '&text_nextframes=' + sequence2);
        } else if (searchMode.value === 'Bert') {
            const sequence1 = document.getElementById('bertQuery').value;
            console.log('Bert Search Query:', bertSearch);
            // Handle search logic for Mode 2 using sequence1 and sequence2
        } else if (searchMode.value === 'Image') {
            const imagePath = document.getElementById('imgQuery').value;
            console.log('Mode 3 Search Query:', bertSearch);
            window.open("/search_image_path?frame_path=" + imagePath)
        }
    });
});

