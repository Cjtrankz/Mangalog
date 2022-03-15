function search_manga(event){
    if(event.keyCode == 13){
        var search = document.getElementById('search').value
        console.log(search)
        fetch(`https://api.mangadex.org/manga?title=${search}&order[relevance]=desc`)
        .then(response => response.json())
        .then(respdata => {
            console.log(respdata);
            
            var search_info = document.querySelector('#manga_info')
            search_info.innerHTML = ["<tr><th>Cover Art</th><th>Title</th><th>Description</th><th>Follow</th></tr>"]
            for (const info of respdata.data){
                fetch(`https://api.mangadex.org/cover/${info.relationships[2].id}`)
                .then(response=>response.json())
                .then(coverdata=> {console.log(coverdata);
                
                search_info.innerHTML += `<tr>
                <td><img class="img-fluid" src="https://uploads.mangadex.org/covers/${info.id}/${coverdata.data.attributes.fileName}" alt=""></img></td>
                <td>${info.attributes.title.en}</td>
                <td>${info.attributes.description.en}</td>
                <td class="align-middle">
                <form action="/follow/process" method='post'>
                    <button type="submit">Follow</button>
                    <input type="hidden" name="dex_id" id="dex_id" value="${info.id}">
                </form></td><tr>`
                console.log(info.id)
                })
            }
        })
        .catch(err => console.log(err) )
    }
}