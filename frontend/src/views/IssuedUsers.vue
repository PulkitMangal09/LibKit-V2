<template>
<div>
<IssuedUsersNav  :bookId="id" />
<table class="table" style="margin-left: auto;">
        <thead>
          <tr class="header">
            <th scope="col">#</th>
            <th scope="col">Request ID</th>
            <th scope="col">Username</th>
            <th scope="col">Name</th>
            <th scope="col">Email</th>
          </tr>
        </thead>
        <tbody class="table-group-divider"   >
          <tr v-for="(data, index) in data" :key="index" class="data">
            <th scope="row">{{index+1}}</th>
            <td>{{data.request_id}}</td>
            <td>{{data.username}}</td>
            <td>{{data.name}}</td>
            <td>{{data.email}}</td>
          </tr>
        </tbody>
</table>
</div>
</template>

<script setup>
import IssuedUsersNav  from '@/components/issued_usersnav.vue';
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';


const route = useRoute();
const router = useRouter();
const id = ref(route.params.id);
const data=ref([]);

const fetchdata = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get(`http://localhost:5000/${id.value}/issued_users`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    data.value = response.data;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      router.push({ name: 'UAView' });
    } else {
      console.error('Error fetching data:', error);
      alert('Failed to fetch data.');
    }
  }
};

onMounted(fetchdata);

</script>

<style scoped>
.table{
  width: 90%;
  margin-left: auto;
  margin-right: auto;
  margin-top: 15px;
}

.header{
  background-color: #f2f2f2;
  text-align: center;
}

.data{
  text-align: center;
}

</style>