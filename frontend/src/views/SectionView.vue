<template>
<div>
<SectionViewNav :sectionId="id"/>
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h1>Section View</h1>
                    <p>View all sections</p>
                    <p>ID: {{ id }}</p>
                </div>
            </div>
    </div>
</div>
</template>

<script setup >
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import SectionViewNav from '@/components/SectionViewNav.vue';

const route = useRoute();
const id = ref(route.params.id);

onMounted(() => {
  // Fetch section data using the id
});
</script>
