function main(){
    console.log("HERE WE ARE !!!")
};

function onSearchKeyUp(event){
    if (event.key != 'Backspace') {
        event.target.parentElement.submit()
    }
};
main();