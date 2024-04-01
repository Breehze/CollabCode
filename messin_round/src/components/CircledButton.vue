<template>
    <div class="relative flex flex-col items-center">
        <button @mouseleave="butHovered = false"  @mouseover="butHovered = true" @click="emitClick()" class="text-lg text-io_light font-semibold cursor-pointer hover:opacity-40 z-10">Proceed</button>    
        <div :class ="{'hovered':butHovered}"  ref="border" class="absolute -top-16 z-0">
            <img  :src="circled" class="w-56" alt="">
        </div>
    </div>
</template>

<script setup>
    import circled from "@/assets/circled.svg"
    import {ref} from 'vue'
    const emit = defineEmits(["bClick"])
    
    const butHovered = ref(false)
    
    const emitClick =() =>{
        emit('bClick')
    }

    

</script>

<style  scoped>
.hovered{
    opacity: 0.4 ;
}

</style>
