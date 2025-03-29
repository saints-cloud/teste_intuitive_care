<template>
  <div class="search-container">
    <h1>Busca de Operadoras</h1>
    
    <div class="search-box">
      <input 
        type="text" 
        v-model="searchTerm" 
        placeholder="Digite o termo de busca (ex: Unimed)"
        @keyup.enter="searchOperadoras"
      >
      <button @click="searchOperadoras">Buscar</button>
    </div>

    <div v-if="loading" class="loading">Carregando...</div>
    
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="results.length > 0" class="results">
      <h2>Resultados</h2>
      <table>
        <thead>
          <tr>
            <th>Registro ANS</th>
            <th>Razão Social</th>
            <th>Nome Fantasia</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in results" :key="index">
            <td>{{ item.Registro_ANS || '-' }}</td>
            <td>{{ item.Razao_Social || '-' }}</td>
            <td>{{ item.Nome_Fantasia || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchOperadoras",
  data() {
    return {
      searchTerm: "",
      results: [],
      loading: false,
      error: null
    };
  },
  methods: {
    async searchOperadoras() {
      if (!this.searchTerm.trim()) {
        this.error = "Por favor, digite um termo de busca";
        return;
      }

      this.loading = true;
      this.error = null;
      
      try {
        const response = await fetch(`http://localhost:8000/search?q=${encodeURIComponent(this.searchTerm)}`);
        
        if (!response.ok) {
          throw new Error("Erro ao buscar operadoras");
        }
        
        this.results = await response.json();
      } catch (err) {
        console.error("Erro na busca:", err);
        this.error = "Erro ao buscar operadoras. Tente novamente.";
        this.results = [];
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.search-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  color: #1fd1ab;
  text-align: center;
}

.search-box {
  display: flex;
  margin: 20px 0;
}

.search-box input {
  flex: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #cfb1b1;
  border-radius: 4px 0 0 4px;
}

.search-box button {
  padding: 10px 20px;
  background-color: #42b983;
  color: ae4242;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 16px;
}

.search-box button:hover {
  background-color: #3aa876;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #e3c8c8;
  padding: 12px;
  text-align: left;
}

th {
  background-color: ae4242;
}

tr:nth-child(even) {
  background-color: ae4242;
}

.loading, .error {
  text-align: center;
  padding: 20px;
  margin: 20px 0;
}

.error {
  color: #e74c3c;
}
</style>