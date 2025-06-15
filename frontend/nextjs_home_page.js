"use client";
import React, { useEffect, useState } from "react";

const PER_PAGE = 20;

export default function NextHome() {
  const [totalRows, setTotalRows] = useState(0);
  const [pages, setPages] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [data, setData] = useState([]);
  const [loadingRows, setLoadingRows] = useState(true);
  const [loadingData, setLoadingData] = useState(false);

  // Fetch total rows once on mount
  useEffect(() => {
    async function fetchRows() {
      try {
        setLoadingRows(true);
        const res = await fetch("http://localhost:5000/rows");
        const text = await res.text();
        // Assuming backend returns number like '66'
        const rows = parseInt(text, 10);
        setTotalRows(rows);
        // calculate pages
        const pageCount = rows % PER_PAGE === 0 ? rows / PER_PAGE : Math.floor(rows / PER_PAGE) + 1;
        setPages(pageCount);
      } catch (err) {
        console.error("Failed to fetch total rows:", err);
      } finally {
        setLoadingRows(false);
      }
    }
    fetchRows();
  }, []);

  // Fetch data for the current page
  useEffect(() => {
    if (pages === 0) return; // no pages, no fetch
    async function fetchData() {
      try {
        setLoadingData(true);
        const res = await fetch(`http://localhost:5000/fetch/${currentPage}`);
        const json = await res.json();
        setData(json);
      } catch (err) {
        console.error("Failed to fetch page data:", err);
        setData([]);
      } finally {
        setLoadingData(false);
      }
    }
    fetchData();
  }, [currentPage, pages]);

  // Function to render pagination with ellipsis if too many pages
  function renderPagination() {
    if (pages <= 7) {
      // render all pages if <=7
      return [...Array(pages)].map((_, i) => (
        <button
          key={i + 1}
          onClick={() => setCurrentPage(i + 1)}
          style={{
            margin: "0 5px",
            fontWeight: currentPage === i + 1 ? "bold" : "normal",
          }}
        >
          {i + 1}
        </button>
      ));
    } else {
      // More than 7 pages: show 1,2,...,current-1,current,current+1,...,last-1,last
      const paginationItems = [];

      // Always show first 2 pages
      paginationItems.push(
        <button
          key={1}
          onClick={() => setCurrentPage(1)}
          style={{ fontWeight: currentPage === 1 ? "bold" : "normal", marginRight: 5 }}
        >
          1
        </button>
      );
      paginationItems.push(
        <button
          key={2}
          onClick={() => setCurrentPage(2)}
          style={{ fontWeight: currentPage === 2 ? "bold" : "normal", marginRight: 5 }}
        >
          2
        </button>
      );

      if (currentPage > 4) paginationItems.push(<span key="left-ellipsis">...</span>);

      // Pages around currentPage
      const start = Math.max(3, currentPage - 1);
      const end = Math.min(pages - 2, currentPage + 1);
      for (let i = start; i <= end; i++) {
        paginationItems.push(
          <button
            key={i}
            onClick={() => setCurrentPage(i)}
            style={{ fontWeight: currentPage === i ? "bold" : "normal", marginRight: 5 }}
          >
            {i}
          </button>
        );
      }

      if (currentPage < pages - 3) paginationItems.push(<span key="right-ellipsis">...</span>);

      // Always show last two pages
      paginationItems.push(
        <button
          key={pages - 1}
          onClick={() => setCurrentPage(pages - 1)}
          style={{ fontWeight: currentPage === pages - 1 ? "bold" : "normal", marginRight: 5 }}
        >
          {pages - 1}
        </button>
      );
      paginationItems.push(
        <button
          key={pages}
          onClick={() => setCurrentPage(pages)}
          style={{ fontWeight: currentPage === pages ? "bold" : "normal" }}
        >
          {pages}
        </button>
      );

      return paginationItems;
    }
  }

  return (
    <div style={{ maxWidth: 800, margin: "auto", padding: 20 }}>
      <h2>Next Home Pagination</h2>
      {loadingRows ? (
        <p>Loading total rows...</p>
      ) : (
        <>
          <p>
            Total rows: {totalRows} | Total pages: {pages}
          </p>
          {loadingData ? (
            <p>Loading data for page {currentPage}...</p>
          ) : (
            <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
              {data.map((item) => (
                <div
                  key={item.id}
                  style={{
                    border: "1px solid #ccc",
                    borderRadius: 5,
                    padding: 10,
                    width: "calc(33% - 10px)",
                    boxSizing: "border-box",
                  }}
                >
                  <h4>{item.name}</h4>
                  <p>{item.description}</p>
                  <img
                    src={item.poster}
                    alt={item.name}
                    style={{ maxWidth: "100%", height: "auto" }}
                  />
                  <a href={item.url} target="_blank" rel="noreferrer">
                    Visit
                  </a>
                </div>
              ))}
            </div>
          )}
          <footer style={{ marginTop: 30, textAlign: "center" }}>{renderPagination()}</footer>
        </>
      )}
    </div>
  );
}
