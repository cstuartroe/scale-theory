package main

import (
	"io"
	"net/http"

	"github.com/cstuartroe/scale-theory/server/lib"
	"github.com/cstuartroe/scale-theory/server/notes"
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	r.LoadHTMLGlob("templates/*")
	r.Static("/static", "./static")
	r.Static("/dist", "./dist")
	r.GET("/api/notes", func(c *gin.Context) {
		var nd notes.NotesDefinition
		if err := c.ShouldBindQuery(&nd); err != nil {
			c.AbortWithStatus(http.StatusBadRequest)
			return
		}

		fb := lib.NewFileBuffer(nil)

		err := notes.CreateNotes(nd, fb)
		if err != nil {
			c.AbortWithError(http.StatusInternalServerError, err)
			return
		}
		fb.Seek(0, io.SeekStart)

		c.DataFromReader(
			http.StatusOK, int64(fb.Len()), "audio/wav", fb, map[string]string{},
		)
	})
	r.NoRoute(
		func(c *gin.Context) {
			c.HTML(
				http.StatusOK,
				"index.tmpl",
				gin.H{},
			)
		},
	)
	r.Run(":9090") // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
}
