var getGithub = document.querySelector('#github_info')
var gitbtn = document.querySelector('#gitbutton')

gitbtn.addEventListener('click', function(){
    fetch("https://api.mangadex.org/manga/d90ea6cb-7bc3-4d80-8af0-28557e6c4e17")
        .then(response => response.json())
        .then(respdata => {
            console.log(respdata);
            var github_info = document.querySelector('#search_results')
            github_info.innerHTML = respdata.data.attributes.title.en //returns "Dungeon Meshi"
            github_info.append(" ", respdata.data.attributes.description.en) //returns "Dungeon Meshi"
            // `<img src="${data}" alt=""></img>`
        })
        .catch(err => console.log(err) )
})