// function populateTable(){
//     var info = document.querySelectorAll(".backlog_info")
//     // var chs_read = document.querySelectorAll(".ch_holder")
//     var ch_titles = document.querySelectorAll(".ch_title")
//     console.log(info)
//     console.log(info[0].innerText)
//     for(let i=0;i<info.length;i++){
//             fetch(`https://api.mangadex.org/manga/${info[i].innerText}`)
//             .then(response => response.json() )
//             .then(respdata => {
//                 console.log(respdata);

//                 fetch(`https://api.mangadex.org/chapter?manga=${info[i].innerText}`)
//                 .then(response => response.json() )
//                 .then(chdata => {console.log(chdata) 

//                 info[i].innerHTML = `${respdata.data.attributes.title.en}`
//                 ch_titles[i].innerHTML = `${chdata.data[0].attributes.chapter} - ${chdata.data[0].attributes.title}`
//                 // info[i].innerHTML += `<td>{{manga.chapters_read}}</td>`
//                 // document.querySelectorAll('.ch_read')[i].innerText = `${chs_read[i]}`
//                 })
                
//                 .catch(err => console.log(err) )
//             })
//             .catch(err => console.log(err) )
//     }
// }