async function getRes() {
    const res = await axios.get(`https://www.themealdb.com/api/json/v1/1/filter.php?i=chicken%20breasts`);
    return res;
}


getRes()