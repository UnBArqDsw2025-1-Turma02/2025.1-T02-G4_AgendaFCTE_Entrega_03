interface Prototype<T> {
  clone(): T;
}

class Evento implements Prototype<Evento> {
  constructor(
    private _id: number,
    private _titulo: string,
    private _descricao: string,
    private _local: string,
    private _categoria: string,
    private _criadoPor: number
  ) {}

  clone(): Evento {
    return new Evento(
      this._id,
      this._titulo,
      this._descricao,
      this._local,
      this._categoria,
      this._criadoPor
    );
  }

  get id() {
    return this._id;
  }
  get titulo() {
    return this._titulo;
  }
  get descricao() {
    return this._descricao;
  }
  get local() {
    return this._local;
  }
  get categoria() {
    return this._categoria;
  }
  get criadoPor() {
    return this._criadoPor;
  }

  set titulo(novoTitulo: string) {
    this._titulo = novoTitulo;
  }
  set descricao(novaDescricao: string) {
    this._descricao = novaDescricao;
  }
  set local(novolocal: string) {
    this._local = novolocal;
  }
}

const eventoOriginal = new Evento(
  1,
  "Rei da Derivada",
  "Evento para treinar habilidade com cálculo 1",
  "Campus FCTE - GAMA/DF",
  "Matemática",
  1001
);

const eventoClonado = eventoOriginal.clone();
eventoClonado.local = "Campus Darcy Ribeiro - BRASÍLIA/DF";

console.log(eventoOriginal);
console.log(eventoClonado);
