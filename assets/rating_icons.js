const get_div = document.getElementById('breweryHolder').children.length - 1
console.log(get_div)

function ratingIcons1() {
    hopFunctions = []
    for(let brewery = 1; brewery < get_div + 1; brewery++){
        for(let hop = 1; hop < 6; hop++){

            if (hop === 1) {

                hopFunctions.push(
                    this[`hop${hop}${brewery}Hover`] = () => {

                        let oneHop = document.getElementById(`rate${hop}${brewery}`)
                        oneHop.style.backgroundImage = "url('/assets/images/green_hop.png')"
                        
                    },

                    this[`hop${hop}${brewery}Exit`] = () => {
                
                        let oneHop = document.getElementById(`rate${hop}${brewery}`)
                        oneHop.style.backgroundImage = "url('/assets/images/white_hop.png')"
                        
                    }
                )
            } else if (hop === 2) {

                hopFunctions.push(
                    this[`hop${hop}${brewery}Hover`] = () => {

                        let oneHop = document.getElementById(`rate${hop - 1}${brewery}`)
                        let twoHop = document.getElementById(`rate${hop}${brewery}`)
                        oneHop.style.backgroundImage = "url('/assets/images/green_hop.png')"
                        twoHop.style.backgroundImage = "url('/assets/images/green_hop.png')"
                        
                    },

                    this[`hop${hop}${brewery}Exit`] = () => {
                
                        let oneHop = document.getElementById(`rate${hop - 1}${brewery}`)
                        let twoHop = document.getElementById(`rate${hop}${brewery}`)
                        oneHop.style.backgroundImage = "url('/assets/images/white_hop.png')"
                        twoHop.style.backgroundImage = "url('/assets/images/white_hop.png')"
                        
                    }

                )
            }  else if (hop === 3) {
                hopFunctions.push(
                    this[`hop${hop}${brewery}Hover`] = () => {

                        let oneHop = document.getElementById(`rate${hop - 2}${brewery}`)
                        let twoHop = document.getElementById(`rate${hop - 1}${brewery}`)
                        let threeHop = document.getElementById(`rate${hop}${brewery}`)
                        oneHop.style.backgroundImage = "url('/assets/images/green_hop.png')"
                        twoHop.style.backgroundImage = "url('/assets/images/green_hop.png')"
                        threeHop.style.backgroundImage = "url('/assets/images/green_hop.png')"
                        
                    },

                    this[`hop${hop}${brewery}Exit`] = () => {
                
                        let oneHop = document.getElementById(`rate${hop - 2}${brewery}`)
                        let twoHop = document.getElementById(`rate${hop - 1}${brewery}`)
                        let threeHop = document.getElementById(`rate${hop}${brewery}`)
                        oneHop.style.backgroundImage = "url('/assets/images/white_hop.png')"
                        twoHop.style.backgroundImage = "url('/assets/images/white_hop.png')"
                        threeHop.style.backgroundImage = "url('/assets/images/white_hop.png')"
                        
                    }

                )
            } else if (hop === 4) {
                hopFunctions.push(
                    this[`hop${hop}${brewery}Hover`] = () => {

                        let oneHop = document.getElementById(`rate${hop - 3}${brewery}`)
                        let twoHop = document.getElementById(`rate${hop - 2}${brewery}`)
                        let threeHop = document.getElementById(`rate${hop -1}${brewery}`)
                        let fourHop = document.getElementById(`rate${hop}${brewery}`)
                        oneHop.style.backgroundImage = "url('/assets/images/green_hop.png')"
                        twoHop.style.backgroundImage = "url('/assets/images/green_hop.png')"
                        threeHop.style.backgroundImage = "url('/assets/images/green_hop.png')"
                        fourHop.style.backgroundImage = "url('/assets/images/green_hop.png')"
                        
                    },

                    this[`hop${hop}${brewery}Exit`] = () => {
                
                        let oneHop = document.getElementById(`rate${hop - 3}${brewery}`)
                        let twoHop = document.getElementById(`rate${hop - 2}${brewery}`)
                        let threeHop = document.getElementById(`rate${hop - 1}${brewery}`)
                        let fourHop = document.getElementById(`rate${hop}${brewery}`)
                        oneHop.style.backgroundImage = "url('/assets/images/white_hop.png')"
                        twoHop.style.backgroundImage = "url('/assets/images/white_hop.png')"
                        threeHop.style.backgroundImage = "url('/assets/images/white_hop.png')"
                        fourHop.style.backgroundImage = "url('/assets/images/white_hop.png')"
                        
                    }
                )
            } else if (hop === 5) {
                hopFunctions.push(
                    this[`hop${hop}${brewery}Hover`] = () => {

                        let oneHop = document.getElementById(`rate${hop - 4}${brewery}`)
                        let twoHop = document.getElementById(`rate${hop - 3}${brewery}`)
                        let threeHop = document.getElementById(`rate${hop -2}${brewery}`)
                        let fourHop = document.getElementById(`rate${hop - 1}${brewery}`)
                        let fiveHop = document.getElementById(`rate${hop}${brewery}`)
                        oneHop.style.backgroundImage = "url('/assets/images/green_hop.png')"
                        twoHop.style.backgroundImage = "url('/assets/images/green_hop.png')"
                        threeHop.style.backgroundImage = "url('/assets/images/green_hop.png')"
                        fourHop.style.backgroundImage = "url('/assets/images/green_hop.png')"
                        fiveHop.style.backgroundImage = "url('/assets/images/green_hop.png')"
                        
                    },

                    this[`hop${hop}${brewery}Exit`] = () => {
                
                        let oneHop = document.getElementById(`rate${hop - 4}${brewery}`)
                        let twoHop = document.getElementById(`rate${hop - 3}${brewery}`)
                        let threeHop = document.getElementById(`rate${hop - 2}${brewery}`)
                        let fourHop = document.getElementById(`rate${hop - 1}${brewery}`)
                        let fiveHop = document.getElementById(`rate${hop}${brewery}`)
                        oneHop.style.backgroundImage = "url('/assets/images/white_hop.png')"
                        twoHop.style.backgroundImage = "url('/assets/images/white_hop.png')"
                        threeHop.style.backgroundImage = "url('/assets/images/white_hop.png')"
                        fourHop.style.backgroundImage = "url('/assets/images/white_hop.png')"
                        fiveHop.style.backgroundImage = "url('/assets/images/white_hop.png')"
                        
                    }
                )
            }
        }
    }
    console.log(hopFunctions)
    return(hopFunctions)
}
ratingIcons1()

