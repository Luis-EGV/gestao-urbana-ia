import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [denuncias, setDenuncias] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");
  const [denunciaSelecionada, setDenunciaSelecionada] = useState(null);

  useEffect(() => {
    carregarDenuncias();
  }, []);

  async function carregarDenuncias() {
    try {
      setCarregando(true);
      setErro("");

      const resposta = await fetch(
        "http://127.0.0.1:8000/gestor/denuncias"
      );

      if (!resposta.ok) {
        throw new Error("Erro ao buscar denúncias");
      }

      const dados = await resposta.json();

      // Ordena do maior IPU para o menor
      const ordenadas = [...dados.denuncias].sort(
        (a, b) => Number(b.ipu) - Number(a.ipu)
      );

      setDenuncias(ordenadas);

    } catch (erro) {
      console.error(erro);
      setErro("Não foi possível conectar com a API.");
    } finally {
      setCarregando(false);
    }
  }

  const total = denuncias.length;

  const recebidas = denuncias.filter(
    (d) => d.status === "Recebida"
  ).length;

  const atendimento = denuncias.filter(
    (d) => d.status === "Em atendimento"
  ).length;

  const risco = denuncias.filter(
    (d) => d.nivel === "Risco"
  ).length;

  return (
    <div className="pagina">

      <header className="topo">
        <div>
          <h1>Painel de Gestão Urbana</h1>
          <p>Monitoramento e priorização de ocorrências urbanas</p>
        </div>
      </header>

      <main className="conteudo">

        <section className="cards">

          <div className="card">
            <span>Total de denúncias</span>
            <strong>{total}</strong>
          </div>

          <div className="card">
            <span>Recebidas</span>
            <strong>{recebidas}</strong>
          </div>

          <div className="card">
            <span>Em atendimento</span>
            <strong>{atendimento}</strong>
          </div>

          <div className="card">
            <span>Nível de risco</span>
            <strong>{risco}</strong>
          </div>

        </section>

        <section className="painel">

          <div className="titulo-painel">
            <div>
              <h2>Fila de ocorrências</h2>
              <p>Ordenadas pelo Índice de Prioridade Urbana (IPU)</p>
            </div>

            <button onClick={carregarDenuncias}>
              Atualizar
            </button>
          </div>

          {carregando && (
            <p className="mensagem">
              Carregando denúncias...
            </p>
          )}

          {erro && (
            <p className="erro">
              {erro}
            </p>
          )}

          {!carregando && !erro && (
            <div className="tabela-container">

              <table>

                <thead>
                  <tr>
                    <th>Protocolo</th>
                    <th>Ocorrência</th>
                    <th>IPU</th>
                    <th>Nível</th>
                    <th>Status</th>
                    <th>Ações</th>
                  </tr>
                </thead>

                <tbody>

                  {denuncias.map((denuncia) => (

                    <tr key={denuncia.id}>

                      <td className="protocolo">
                        {denuncia.protocolo}
                      </td>

                      <td>
                        <strong>
                          {denuncia.classe_yolo || "Não identificada"}
                        </strong>

                        <small>
                          {denuncia.descricao}
                        </small>
                      </td>

                      <td>
                        <span className="ipu">
                          {denuncia.ipu}
                        </span>
                      </td>

                      <td>
                        <span
                          className={`nivel ${denuncia.nivel
                            ?.toLowerCase()
                            .replace(" ", "-")}`}
                        >
                          {denuncia.nivel}
                        </span>
                      </td>

                      <td>
                        {denuncia.status}
                      </td>

                      <td>
                        <button
                          className="botao-detalhes"
                          onClick={() => setDenunciaSelecionada(denuncia)}>
                          Ver detalhes
                        </button>
                      </td>

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>
          )}

        </section>

      </main>

          {denunciaSelecionada && (
            <div className="modal-fundo">

              <div className="modal">

                <div className="modal-topo">

                  <div>
                    <h2>Detalhes da ocorrência</h2>
                    <p>{denunciaSelecionada.protocolo}</p>
                  </div>

                  <button
                    className="fechar"
                    onClick={() => setDenunciaSelecionada(null)}
                  >
                    ✕
                  </button>

                </div>

                {denunciaSelecionada.imagem_url ? (
                  <img
                    className="imagem-denuncia"
                    src={`http://127.0.0.1:8000${denunciaSelecionada.imagem_url}`}
                    alt="Imagem da denúncia"
                  />
                ) : (
                  <div className="sem-imagem">
                    Imagem não disponível
                  </div>
                )}

                <div className="detalhes-grid">

                  <div>
                    <span>Ocorrência</span>
                    <strong>
                      {denunciaSelecionada.classe_yolo || "Não identificada"}
                    </strong>
                  </div>

                  <div>
                    <span>IPU</span>
                    <strong>
                      {denunciaSelecionada.ipu}
                    </strong>
                  </div>

                  <div>
                    <span>Nível</span>
                    <strong>
                      {denunciaSelecionada.nivel}
                    </strong>
                  </div>

                  <div>
                    <span>Status</span>
                    <strong>
                      {denunciaSelecionada.status}
                    </strong>
                  </div>

                  <div>
                    <span>Latitude</span>
                    <strong>
                      {denunciaSelecionada.latitude}
                    </strong>
                  </div>

                  <div>
                    <span>Longitude</span>
                    <strong>
                      {denunciaSelecionada.longitude}
                    </strong>
                  </div>

                </div>

                <div className="descricao-detalhes">

                  <span>Descrição do cidadão</span>

                  <p>
                    {denunciaSelecionada.descricao}
                  </p>

                </div>

                <div className="analise-ia">

                  <h3>Análise da IA</h3>

                  <div className="detalhes-grid">

                    <div>
                      <span>Confiança YOLO</span>
                      <strong>
                        {denunciaSelecionada.confianca_yolo}
                      </strong>
                    </div>

                    <div>
                      <span>Risco da imagem</span>
                      <strong>
                        {denunciaSelecionada.risco_imagem}
                      </strong>
                    </div>

                    <div>
                      <span>Risco do texto</span>
                      <strong>
                        {denunciaSelecionada.risco_texto}
                      </strong>
                    </div>

                    <div>
                      <span>Risco do contexto</span>
                      <strong>
                        {denunciaSelecionada.risco_contexto}
                      </strong>
                    </div>

                  </div>

                </div>

              </div>

            </div>
          )}

    </div>
  );
}

export default App;