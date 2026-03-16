import { useEffect, useState } from 'react'
import api from './api'
import { User, Mail, Phone, Plus, X, Trash2, Pencil} from 'lucide-react'

export default function App() {
  const [pacientes, setPacientes] = useState([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [novoPaciente, setNovoPaciente] = useState({ nome: '', email: '', telefone: '' })
  const [pacienteEmEdicao, setPacienteEmEdicao] = useState(null) // null = criando novo, {objeto} = editando

  // Busca os pacientes
  const carregarPacientes = () => {
    api.get('/pacientes/')
      .then(res => setPacientes(res.data))
      .catch(err => console.error(err))
  }

  const prepararEdicao = (paciente) => {
  setPacienteEmEdicao(paciente); // Salva quem estamos editando
  setNovoPaciente({
    nome: paciente.nome,
    email: paciente.email,
    telefone: aplicarMascaraTelefone(paciente.telefone)
  });
  setIsModalOpen(true);
};
  

  useEffect(() => { carregarPacientes() }, [])

  const handleSubmit = async (e) => {
  e.preventDefault()
  const numerosPuros = novoPaciente.telefone.replace(/\D/g, '')

  try {
    if (pacienteEmEdicao) {
      // MODO EDIÇÃO: Usa o método PUT
      await api.put(`/pacientes/${pacienteEmEdicao.id}`, { ...novoPaciente, telefone: numerosPuros })
    } else {
      // MODO CRIAÇÃO: Usa o método POST
      await api.post('/pacientes/', { ...novoPaciente, telefone: numerosPuros })
    }
    
    fecharModal()
    carregarPacientes()
  } catch (err) {
    alert("Erro ao salvar dados.")
  }
}

  // Função para aplicar a máscara (99) 99999-9999
  const aplicarMascaraTelefone = (valor) => {
    if (!valor) return ""
    valor = valor.replace(/\D/g, "") // Remove tudo que não é número
    valor = valor.replace(/(\d{2})(\d)/, "($1) $2") // Coloca parênteses no DDD
    valor = valor.replace(/(\d{5})(\d)/, "$1-$2") // Coloca o hífen
    return valor.substring(0, 15) // Limita o tamanho visual
  }

  const deletarPaciente = async (id) => {
  if (window.confirm("Tem certeza que deseja excluir este paciente?")) {
    try {
      await api.delete(`/pacientes/${id}`)
      carregarPacientes() // Atualiza a lista após deletar
    } catch (err) {
      alert("Erro ao excluir paciente.")
    }
  }
}

  const abrirModalNovo = () => {
    setPacienteEmEdicao(null); // Garante que NÃO estamos em modo edição
    setNovoPaciente({ nome: '', email: '', telefone: '' }); // Limpa o formulário
    setIsModalOpen(true);
  };

const fecharModal = () => {
  setIsModalOpen(false);
  setPacienteEmEdicao(null);
  setNovoPaciente({ nome: '', email: '', telefone: '' });
};
  

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        
        {/* Cabeçalho */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 italic">DentalMax</h1>
          <button 
            onClick={abrirModalNovo}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition"
          >
            <Plus size={20} /> Novo Paciente
          </button>
        </div>

        {/* Tabela de Pacientes (mesmo código anterior) */}
        <div className="bg-white rounded-xl shadow-md overflow-hidden border border-gray-200">
          <table className="w-full text-left">
            <thead className="bg-gray-100 border-b border-gray-200">
              <tr>
                <th className="px-6 py-4 text-sm font-semibold text-gray-600 uppercase">Paciente</th>
                <th className="px-6 py-4 text-sm font-semibold text-gray-600 uppercase">Contato</th>
                <th className="px-6 py-4 text-sm font-semibold text-gray-600 uppercase text-right">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {pacientes.map(p => (
                <tr key={p.id} className="hover:bg-gray-50 transition">
                  <td className="px-6 py-4 font-medium text-gray-700">{p.nome}</td>
                  <td className="px-6 py-4 text-sm text-gray-500">{p.email} | {p.telefone}</td>
                  <td className="px-6 py-4 text-right space-x-2">
                    <button 
                      onClick={() => prepararEdicao(p)}
                      className="text-blue-600 hover:text-blue-800 transition"
                      title='Editar'
                    >
                      <Pencil size={18} />
                    </button>
                    <button 
                      onClick={() => deletarPaciente(p.id)}
                      className="text-red-500 hover:text-red-700 transition"
                      title='Excluir'
                    >
                      <Trash2 size={18} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* MODAL DE CADASTRO */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold">
                {pacienteEmEdicao ? 'Editar Paciente' : 'Cadastrar Paciente'}
                </h2>
              <button onClick={fecharModal} className="text-gray-400 hover:text-gray-600">
                <X size={24} />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Nome Completo</label>
                <input 
                  required
                  className="w-full mt-1 p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 outline-none"
                  value={novoPaciente.nome}
                  onChange={e => setNovoPaciente({...novoPaciente, nome: e.target.value})}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">E-mail</label>
                <input 
                  type="email" required
                  className="w-full mt-1 p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 outline-none"
                  value={novoPaciente.email}
                  onChange={e => setNovoPaciente({...novoPaciente, email: e.target.value})}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Telefone</label>
                <input 
                  required
                  placeholder="(99) 99999-9999"
                  className="w-full mt-1 p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 outline-none"
                  value={novoPaciente.telefone}
                  onChange={e => setNovoPaciente({
                    ...novoPaciente, 
                    telefone: aplicarMascaraTelefone(e.target.value)
                  })}
                />
              </div>
              <button type="submit" className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold hover:bg-blue-700 transition">
                {pacienteEmEdicao ? 'Salvar Alterações' : 'Salvar Paciente'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
