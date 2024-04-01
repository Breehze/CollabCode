<template>
        <div class="flex-row relative w-11/12 h-72 sm:h-96 mt-0">
            <div class=" flex items-center w-full bg-io_mid_dark h-5 rounded-t-lg">
                <div class="rounded-full w-2 h-2 bg-red-400 ml-1"></div> 
                <div class="rounded-full w-2 h-2 bg-yellow-600 ml-1"></div>
                <div class="rounded-full w-2 h-2 bg-green-400 ml-1"></div>

            </div>
            <div  class="w-full h-full  absolute z-10 bg-transparent">
                <textarea ref="master" :value = "join(doc)"  @scroll="syncScroll()" @paste = "(event) => paste(event)" @keydown="(event) => {sendAction(event)}" id="textIn" spellcheck="false" autocomplete="off" class="text-transparent outline-none bg-transparent w-full h-full font-mono  p-2 text-xs  bg-opacity-100 caret-black" ></textarea>     
            </div>
            <pre ref= "slave"  class="absolute z-0 l-0 t-0 bg-io_mid_light w-full h-full overflow-auto font-mono text-xs p-2 rounded-b-lg line"><code ref="code" id="code" class="language-python bg-transparent !p-0" >{{join(doc)}}</code></pre>   
        </div>
</template>

<script setup>
    import {ref,defineProps,onMounted,watch, nextTick} from 'vue'  
    import hljs from 'highlight.js/lib/core'
    import 'highlight.js/styles/github.css'; // Example style, pick one you like

    import python from 'highlight.js/lib/languages/python'


    hljs.registerLanguage("python",python)

    const props = defineProps({webSocket: Object})
    const doc = ref([[]])

    let initial_accept = true

    watch(doc,()=>{
        nextTick(() => {
            const highlightee = document.getElementById('code')
            if(highlightee){
                highlightee.removeAttribute('data-highlighted') 
                hljs.highlightElement(highlightee)
                console.log("highlight")
            }
        })
         
    },{deep : true})

    const master = ref(null)
    const slave = ref(null)
    const code = ref(null)

    const syncScroll = () =>{
        slave.value.scrollTop = master.value.scrollTop
        slave.value.scrollLeft = master.value.scrollLeft
    }

    

    
    
    const getCursorPos = () => {
        const textarea = document.getElementById("textIn")
        const text = textarea.value;
        const selectionPoint = textarea.selectionStart;
        const upToSelection = text.substring(0, selectionPoint);
        const rows = (upToSelection.match(/\n/g) || []).length + 1;
        const lastNewlineIndex = upToSelection.lastIndexOf('\n');
        const cols = selectionPoint - lastNewlineIndex;
        return [rows-1,cols-2]
    }

    const disjoin = (str) =>{
        const lines = str.split('\n');
        const matrix = lines.map(line => line.split(''));
        return matrix; 
    }

    const join = (matrix) =>{
        return matrix.map(row => row.join('')).join('\n')
    }

    onMounted(()=>{
        props.webSocket.addEventListener("message",(event)=>{
            if (initial_accept) {
                doc.value = JSON.parse(event.data)
                initial_accept = false
                return
            }
            let parsed = JSON.parse(event.data)
            if (parsed.operation == "Nline"){
                    doc.value.splice(parsed.cords[0],0,parsed.content)
                    return
            }
            if (parsed.operation == "Delete"){
                if(doc.value.length == 0){
                    return
                }
                if(parsed.cords[1] == doc.value[parsed.cords[0]].length - 1){
                    doc.value.splice(parsed.cords[0]+1,1)
                    return
                }
                doc.value[parsed.cords[0]].splice(parsed.cords[1]+1,1) 
                return
            }
            if(parsed.operation == "Paste"){
                let line = doc.value[parsed.cords[0]]
                if(parsed.content.length == 1){
                    doc.value[parsed.cords[0]] = [...line.slice(0,parsed.cords[1]+1),...parsed.content[0],...line.slice(parsed.cords[1]+1)]
                }else{
                    let start = doc.value[parsed.cords[0]].slice(0,parsed.cords[1]+1)
                    let end = doc.value[parsed.cords[0]].slice(parsed.cords[1]+1)
                    let j = 1
                    doc.value[parsed.cords[0]] = [...start,...parsed.content[0]]
                    for(let i = parsed.cords[0]+ 1 ;i< parsed.cords[0] + parsed.content.length;i++){
                        doc.value.splice(i,0,parsed.content[j]) 
                        j++
                    }
                } 
                return
            }
            doc.value[parsed.cords[0]].splice(parsed.cords[1],0,parsed.content)
        })    
    })

    const sendAction = (event) => {
        setTimeout(() =>{ 
            syncScroll()
            let header = {
                operation : "insert",
                cords : getCursorPos(),
                content : event.key
            } 
            if (event.key == "Backspace"){
                header.operation = "Delete"
                header.content = ""
            }else if (event.key == "Enter"){
                header.operation = "Nline"
                header.content = []
            }
            if (header.content.length > 1 || (event.ctrlKey && header.content == 'v') ){
                console.log("hello")
                return
            }  
            props.webSocket.send(JSON.stringify(header))
            doc.value = disjoin(master.value.value)
        },1)
    }

    const paste = (event) => {
        let pasted = (event.clipboardData || window.clipboardData).getData("text") 
        let header = {
            operation : "Paste",
            cords : getCursorPos(),
            content : disjoin(pasted)  
        }
        props.webSocket.send(JSON.stringify(header))
    }

</script>
