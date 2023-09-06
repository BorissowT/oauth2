export interface Room {
    name?: string;
    id: number,
    price: number,
    label: LabelLanguages,
    colors?: [{
        color: string,
        price: number,
        id: number,
    }],
}

export interface LabelLanguages {
    de: string,
    en: string,
}