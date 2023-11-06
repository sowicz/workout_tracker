const appBtn = document.getElementById("app-button");

appBtn.style.border = "thin solid white";




// this below code is attached to excercise.html 
// there is function for:
// - add series button "+"
// - delete exercise "del"
// - edit exercise name "edit"


  function seriesAdd(bp, ex) {
    seriesdiv = htmx.find(`.series`)
    htmx.ajax('GET', `/addseries/${bp}/${ex}`, {target: seriesdiv, swap:'beforeend'})
  }
  
  function delExercise(id, ex) {
    const removebtn = document.querySelector(`[class="${id}"]`)
    if (confirm(`Are you sure you want to delete: ${id}?`) == true) {
      fetch(`/deleteexercise/${ex}`, { method: "DELETE" })
          .then((response) => {
              const elementToRemove = document.querySelector(`[id="${id}"]`)
              elementToRemove.parentElement.remove()
            })
            .catch((error) => console.log(error));
          } 
  };

  // take id to edit input value (exercise name)
  function edit(id, bp, ex) {
      console.log("edit function called")
  
      const elementToEdit = document.querySelector(`[id="${id}"]`);
      const el = elementToEdit.firstElementChild
      const editBtn = elementToEdit.children[1]
      editBtn.innerHTML = "OK"


      el.setAttribute("contenteditable", "True");
      el.style.borderColor = "yellow";
      editBtn.removeAttribute("onclick")
      editBtn.setAttribute("onclick", `confirmedit('${id}','${bp}','${ex}')` )

  };

  function confirmedit(id, bp, ex) {
    console.log("confirm function called")
    const elementToEdit = document.querySelector(`[id="${id}"]`);

    let exNew = elementToEdit.firstElementChild.innerHTML;
    exNew = exNew.trim();

    // check if any input has the same name as edited input
    // to prevent the same exercise name 
    let exToCheck = document.querySelectorAll("div#excerciseContainer")

    let ar = []
    let count = 0
    let exExist = false

    for (let i=0; i< exToCheck.length; i++){
      ar.push(exToCheck[i].innerHTML.trim())
      if (exNew == exToCheck[i].innerHTML.trim()) {
        count++;
        if (count == 2) {
          console.log("wartość wystepuje 2 razy")
          const el = elementToEdit.firstElementChild
          el.style.borderColor = "red";
          exExist = true
        }

      }
    }
    if (!exExist) {
        // fetching data to edit exercise name
        const el = elementToEdit.firstElementChild
        const editBtn = elementToEdit.children[1]
        const delBtn = elementToEdit.children[2]
        const addSeriesBtn = document.querySelector(`[id="range-${ex}"]`).lastElementChild
        const rangediv = document.querySelector(`[id="range-${ex}"]`)

        fetch(`/edit/${bp}/${ex}/${exNew}`, { method: "PUT" })
        .then((response) => {
        
        editBtn.innerHTML = "Edit"

        el.style.borderColor = "";
        elementToEdit.setAttribute("id",`${bp}-${exNew}`)
        
        el.setAttribute("contenteditable", "false");
        editBtn.removeAttribute("onclick")
        editBtn.setAttribute("onclick", `edit('${bp}-${exNew}','${bp}','${exNew}')` )
        delBtn.setAttribute("onclick", `delExercise('${bp}-${exNew}','${exNew}')`)
        
        addSeriesBtn.setAttribute("hx-get", `/addseries/${bp}/${exNew}`)
        rangediv.setAttribute("id", `range-${exNew}`)
        htmx.process(addSeriesBtn)


        //take series elements for edit to new exercise name
        let seriesElements = document.querySelector((`[id="series-${ex}"]`))
        let sElement = seriesElements.querySelectorAll(".set")
        // update name of existing series button: "OK" and "X"
        sElement.forEach( (el, index)=> {
          seriesElements.setAttribute("id",`series-${exNew}`)
          el.parentElement.parentElement.id = `${exNew}-series-${index+1}`
          el.parentElement.lastElementChild.setAttribute("onclick",`delSeries('${exNew}-series-${index+1}', '${bp}','${exNew}','${index+1}')`)
          el.parentElement[2].setAttribute("hx-post", `/addseriesdata/${bp}/${exNew}/${index+1}`)
          
          htmx.process(el.parentElement[2])
        })
      
        })
    }

  }


// here is end script part for excercise.html 
// --------------------------------------------------
// -------------------------------------------------



// below part is for series.html
// there is function:
// - delete series "x" - button


function delSeries(id, bp, ex, sr) {
  // console.log(`id: ${id}`)
  // console.log(`bp: ${bp}`)
  // console.log(`ex: ${ex}`)
  // console.log(`sr: ${sr}`)
  const delDiv = document.querySelector((`[id="${id}"]`))
  let seriesElements = document.querySelector((`[id="series-${ex}"]`))

  fetch(`/deleteseries/${bp}/${ex}/${sr}`, { method: "DELETE" })
        .then((response) => {

            delDiv.remove()
            let sElement = seriesElements.querySelectorAll(".set")

            // change innerhtml for all elements
            sElement.forEach( (el, index)=> {
              el.innerHTML = `Series [${index+1}]`
              el.parentElement.parentElement.id = `${ex}-series-${index+1}`
              el.parentElement.lastElementChild.setAttribute("onclick",`delSeries('${ex}-series-${index+1}', '${bp}','${ex}','${index+1}')`)
              el.parentElement[2].setAttribute("hx-post", `/addseriesdata/${bp}/${ex}/${index+1}`)

              htmx.process(el.parentElement[2])
            })

            
        })
        .catch((error) => console.log(error));
}


// end part for series.html
// --------------------------------------------------
// -------------------------------------------------