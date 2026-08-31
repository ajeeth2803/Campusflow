<template>
  <div style="max-width: 900px; margin: 0 auto; font-family: sans-serif; padding: 20px;">
    <header style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #ddd; padding-bottom: 15px;">
      <h1 style="margin: 0;">CampusFlow MVP</h1>
      <div>
        <select v-model="currentRole" style="padding: 6px; font-weight: bold;">
          <option value="STUDENT">Student (Raise Request)</option>
          <option value="STAFF">Staff / Admin (Manage Tickets)</option>
        </select>
      </div>
    </header>

    <!-- STUDENT VIEW -->
    <section v-if="currentRole === 'STUDENT'" style="margin-top: 25px;">
      <h2>Raise a Service Request</h2>
      <form @submit.prevent="submitTicket" style="display: flex; flex-direction: column; gap: 12px; max-width: 500px;">
        <input v-model="form.title" placeholder="Request Title (e.g., Lab 3 Projector Down)" required style="padding: 10px;" />
        
        <select v-model="form.category" required style="padding: 10px;">
          <option value="" disabled>Select Department</option>
          <option value="IT">IT Services</option>
          <option value="Maintenance">Maintenance</option>
          <option value="Hostel">Hostel Services</option>
          <option value="Admin">Academic Administration</option>
        </select>

        <select v-model="form.priority" style="padding: 10px;">
          <option value="LOW">Low Priority</option>
          <option value="MEDIUM">Medium Priority</option>
          <option value="HIGH">High Priority</option>
        </select>

        <textarea v-model="form.description" placeholder="Detail the issue..." rows="4" style="padding: 10px;"></textarea>

        <button type="submit" style="padding: 12px; background: #007bff; color: white; border: none; font-weight: bold; cursor: pointer;">
          Submit Request
        </button>
      </form>
    </section>

    <!-- STAFF / ADMIN VIEW -->
    <section v-else style="margin-top: 25px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
        <h2>Department Workload Queue</h2>
        <button @click="fetchTickets" style="padding: 8px 16px; cursor: pointer;">Refresh Data</button>
      </div>

      <table border="1" cellpadding="10" cellspacing="0" style="width: 100%; border-collapse: collapse; text-align: left;">
        <thead>
          <tr style="background: #f4f4f4;">
            <th>ID</th>
            <th>Title & Description</th>
            <th>Category</th>
            <th>Priority</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ticket in tickets" :key="ticket.id">
            <td>#{{ ticket.id }}</td>
            <td>
              <strong>{{ ticket.title }}</strong><br/>
              <small style="color: #666;">{{ ticket.description }}</small>
            </td>
            <td>{{ ticket.category }}</td>
            <td>{{ ticket.priority }}</td>
            <td>
              <strong :style="{ color: ticket.status === 'RESOLVED' ? 'green' : (ticket.status === 'IN_PROGRESS' ? 'orange' : 'red') }">
                {{ ticket.status }}
              </strong>
            </td>
            <td>
              <button v-if="ticket.status === 'OPEN'" @click="updateStatus(ticket.id, 'IN_PROGRESS')" style="margin-right: 5px; padding: 5px 10px;">
                In Progress
              </button>
              <button v-if="ticket.status !== 'RESOLVED'" @click="updateStatus(ticket.id, 'RESOLVED')" style="padding: 5px 10px; background: #28a745; color: white; border: none;">
                Resolve
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:5000/api/tickets'
const currentRole = ref('STUDENT')
const tickets = ref([])

const form = ref({
  title: '',
  category: '',
  priority: 'MEDIUM',
  description: ''
})

const fetchTickets = async () => {
  try {
    const res = await axios.get(API_URL)
    tickets.value = res.data
  } catch (err) {
    console.error('Connection error:', err)
  }
}

const submitTicket = async () => {
  try {
    await axios.post(API_URL, form.value)
    alert('Request created successfully!')
    form.value = { title: '', category: '', priority: 'MEDIUM', description: '' }
    fetchTickets()
  } catch (err) {
    alert('Failed to submit ticket')
  }
}

const updateStatus = async (id, status) => {
  try {
    await axios.patch(`${API_URL}/${id}`, { status })
    fetchTickets()
  } catch (err) {
    alert('Failed to update ticket status')
  }
}

onMounted(() => {
  fetchTickets()
})
</script>
<style>
/* Global Page Background */
body {
  margin: 0;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
  color: #f8fafc;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
}

/* Card Container */
.app-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

/* Vibrant Inputs & Selects */
input, select, textarea {
  background: rgba(255, 255, 255, 0.08) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  color: #fff !important;
  border-radius: 8px !important;
  outline: none;
}

input::placeholder, textarea::placeholder {
  color: #94a3b8;
}

/* Eye-Catching Action Button */
button[type="submit"] {
  background: linear-gradient(45deg, #6366f1, #a855f7) !important;
  color: white !important;
  border-radius: 8px !important;
  font-weight: bold;
  letter-spacing: 0.5px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

button[type="submit"]:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(168, 85, 247, 0.4);
}
<style>
/* Global Page Background */
body {
  margin: 0;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
  color: #f8fafc;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
}

/* Card Container */
.app-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

/* Vibrant Inputs & Selects */
input, select, textarea {
  background: rgba(255, 255, 255, 0.08) !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  color: #fff !important;
  border-radius: 8px !important;
  outline: none;
}

input::placeholder, textarea::placeholder {
  color: #94a3b8;
}

/* Eye-Catching Action Button */
button[type="submit"] {
  background: linear-gradient(45deg, #6366f1, #a855f7) !important;
  color: white !important;
  border-radius: 8px !important;
  font-weight: bold;
  letter-spacing: 0.5px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

button[type="submit"]:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(168, 85, 247, 0.4);
}
/* Fix for invisible dropdown options */
select option {
  background-color: #1e1b4b !important;
  color: #ffffff !important;
  padding: 10px;
}
</style>
